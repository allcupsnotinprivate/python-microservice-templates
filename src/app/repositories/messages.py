import abc
from typing import Sequence

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Message

from .aClasses import ARepository


class AMessagesRepository(ARepository[Message, int], abc.ABC):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Message)

    @abc.abstractmethod
    async def get_conversation_messages(self, conversation_id: int, page: int, per_page: int) -> Sequence[Message]:
        raise NotImplementedError


class MessagesRepository(AMessagesRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_conversation_messages(self, conversation_id: int, page: int, per_page: int) -> Sequence[Message]:
        offset = (page - 1) * per_page

        if per_page <= 0:
            return []

        stmt = (
            select(self.model_class)
            .where(Message.conversation_id == conversation_id)
            .order_by(desc(self.model_class.created_at))
            .offset(offset)
            .limit(per_page)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
