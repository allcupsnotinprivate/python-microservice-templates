from datetime import datetime

from pydantic import Field

from app.utils.schemas import BaseAPISchema


class ConversationOut(BaseAPISchema):
    id: int
    created_at: datetime


class MessageIn(BaseAPISchema):
    content: str
    reply_to: int | None = Field(default=None)


class MessageOut(BaseAPISchema):
    id: int
    created_at: datetime
    author: str
    content: str
    reply_to: int | None
