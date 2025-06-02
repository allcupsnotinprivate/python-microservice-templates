import abc
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Conversation

from .aClasses import ARepository


class AConversationsRepository(ARepository[Conversation, int], abc.ABC):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Conversation)

    @abc.abstractmethod
    async def search(self, page: int, per_page: int) -> Sequence[Conversation]:
        raise NotImplementedError


class ConversationsRepository(AConversationsRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def search(self, page: int, per_page: int) -> Sequence[Conversation]:
        offset = (page - 1) * per_page

        if per_page <= 0:
            return []

        stmt = select(self.model_class).order_by(self.model_class.created_at).offset(offset).limit(per_page)
        result = await self.session.execute(stmt)
        return result.scalars().all()
