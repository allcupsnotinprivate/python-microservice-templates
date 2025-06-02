import abc
from typing import Collection, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
IdentifierType = TypeVar("IdentifierType")


class ARepository[ModelType, IdentifierType](abc.ABC):
    def __init__(self, session: AsyncSession, model_class: type[ModelType]):
        self.session = session
        self.model_class = model_class

    async def add(self, item: ModelType) -> None:
        self.session.add(item)
        await self.session.flush((item,))

    async def add_many(self, items: Collection[ModelType]) -> None:
        self.session.add_all(items)

    async def get(self, id: IdentifierType) -> ModelType | None:
        item = await self.session.get(self.model_class, id)
        return item

    async def delete(self, id: IdentifierType) -> bool:
        item = await self.get(id)
        if item:
            await self.session.delete(item)
            return True
        return False
