import abc
from typing import Sequence

from app import exceptions
from app.models import Conversation, Message

from .aClasses import AService
from .uow import AUnitOfWork


class AConversationsService(AService, abc.ABC):
    @abc.abstractmethod
    async def create(self) -> Conversation:
        raise NotImplementedError

    @abc.abstractmethod
    async def search(self, page: int, per_page: int) -> Sequence[Conversation]:
        raise NotImplementedError

    @abc.abstractmethod
    async def read(self, conversation_id: int, page: int, per_page: int) -> Sequence[Message]:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, conversation_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def send_message(
        self,
        conversation_id: int,
        author: str,
        content: str,
        reply_to: int | None = None,
    ) -> Message:
        raise NotImplementedError


class ConversationsService(AConversationsService):
    def __init__(self, uow: AUnitOfWork):
        self.uow = uow

    async def create(self) -> Conversation:
        async with self.uow as uow_ctx:
            conversation = Conversation()
            await uow_ctx.conversations.add(conversation)
        return conversation

    async def search(self, page: int, per_page: int) -> Sequence[Conversation]:
        async with self.uow as uow_ctx:
            conversations = await uow_ctx.conversations.search(page, per_page)
        return conversations

    async def read(self, conversation_id: int, page: int, per_page: int) -> Sequence[Message]:
        async with self.uow as uow_ctx:
            conversations = await uow_ctx.messages.get_conversation_messages(conversation_id, page, per_page)
        return conversations

    async def delete(self, conversation_id: int) -> None:
        async with self.uow as uow_ctx:
            is_deleted = await uow_ctx.conversations.delete(conversation_id)
        if not is_deleted:
            raise exceptions.DataError("Failed to delete conversation.")

    async def send_message(
        self, conversation_id: int, author: str, content: str, reply_to: int | None = None
    ) -> Message:
        async with self.uow as uow_ctx:
            conversation = await uow_ctx.conversations.get(conversation_id)
            if not conversation:
                raise exceptions.NotFoundError(f"Not found conversation with id={conversation_id}")
            message = Message(author=author, content=content, reply_to=reply_to, conversation_id=conversation_id)
            await uow_ctx.messages.add(message)
        return message
