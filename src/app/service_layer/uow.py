import abc
from contextlib import AbstractAsyncContextManager
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app import repositories
from app.infrastructure import APostgresDatabase


class AUnitOfWorkContext(abc.ABC):
    conversations: repositories.AConversationsRepository
    messages: repositories.AMessagesRepository

    @abc.abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class UnitOfWorkContext(AUnitOfWorkContext):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.conversations = repositories.ConversationsRepository(self.session)
        self.messages = repositories.MessagesRepository(self.session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


class AUnitOfWork(abc.ABC):
    @abc.abstractmethod
    async def __aenter__(self) -> AUnitOfWorkContext: ...

    @abc.abstractmethod
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None: ...


class UnitOfWork(AUnitOfWork):
    def __init__(self, postgres_database: APostgresDatabase):
        self.session_factory = postgres_database.get_session
        self._session_cm: AbstractAsyncContextManager[AsyncSession] | None = None
        self._context: AUnitOfWorkContext | None = None

    async def __aenter__(self) -> AUnitOfWorkContext:
        self._session_cm = self.session_factory()
        self.session = await self._session_cm.__aenter__()
        self._context = UnitOfWorkContext(self.session)
        return self._context

    async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any) -> None:
        if self._context:
            try:
                if exc_type:
                    await self._context.rollback()
                else:
                    await self._context.commit()
            finally:
                if self._session_cm:
                    await self._session_cm.__aexit__(exc_type, exc_val, exc_tb)
                self._session_cm = None
