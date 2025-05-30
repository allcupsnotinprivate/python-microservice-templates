from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Body, Depends, Path, Query, Request

from app.exceptions import PermissionDeniedError
from app.service_layer import AConversationsService

from .schemas import ConversationOut, MessageIn, MessageOut

router = APIRouter()


@router.post("/conversations", status_code=201, response_model=ConversationOut)
@inject
async def create_conversation(conversations_service: Injected[AConversationsService] = Depends()) -> ConversationOut:
    conversation = await conversations_service.create()
    result = ConversationOut(id=conversation.id, created_at=conversation.created_at)
    return result


@router.get("/conversations", status_code=200, response_model=list[ConversationOut])
@inject
async def search_conversations(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, alias="perPage"),
    conversations_service: Injected[AConversationsService] = Depends(),
) -> list[ConversationOut]:
    conversations = await conversations_service.search(page, per_page)
    result = [ConversationOut(id=conversation.id, created_at=conversation.created_at) for conversation in conversations]
    return result


@router.delete("/conversations/{conversationId}", status_code=204)
@inject
async def delete_conversation(
    conversation_id: int = Path(alias="conversationId"),
    conversations_service: Injected[AConversationsService] = Depends(),
) -> None:
    await conversations_service.delete(conversation_id)
    return


@router.get("/conversations/{conversationId}/messages", status_code=200, response_model=list[MessageOut])
@inject
async def read_conversation(
    conversation_id: int = Path(alias="conversationId"),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, alias="perPage"),
    conversations_service: Injected[AConversationsService] = Depends(),
) -> list[MessageOut]:
    messages = await conversations_service.read(conversation_id, page, per_page)
    result = [
        MessageOut(id=msg.id, created_at=msg.created_at, author=msg.author, content=msg.content, reply_to=msg.reply_to)
        for msg in messages
    ]
    return result


@router.post("/conversations/{conversationId}/messages", status_code=201, response_model=MessageOut)
@inject
async def send_message_to_conversation(
    request: Request,
    conversation_id: int = Path(alias="conversationId"),
    data: MessageIn = Body(),
    conversations_service: Injected[AConversationsService] = Depends(),
) -> MessageOut:
    if request.client:
        author = str(request.client.host)
    else:
        raise PermissionDeniedError("Unable to identify client")

    message = await conversations_service.send_message(conversation_id, author, data.content, data.reply_to)
    result = MessageOut(
        id=message.id,
        created_at=message.created_at,
        author=message.author,
        content=message.content,
        reply_to=message.reply_to,
    )
    return result
