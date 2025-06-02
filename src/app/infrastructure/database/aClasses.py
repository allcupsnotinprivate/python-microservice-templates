import abc
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import URL, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.infrastructure.aClasses import AInfrastructure
from app.models import Base

from .migrations.config import AlembicConfig
from .migrations.manager import AlembicManager


class ASQLDatabase(AInfrastructure, abc.ABC):
    def __init__(
        self,
        driver: str,
        user: str,
        password: str,
        host: str,
        port: int,
        database: str,
        automigrate: bool,
    ):
        self.automigrate = automigrate
        self.url = URL.create(
            username=user, password=password, host=host, port=port, database=database, drivername=driver
        )
        self.engine = create_async_engine(self.url, echo=False)
        self.Session = async_sessionmaker(bind=self.engine, autoflush=True, expire_on_commit=False)
        self.Base = Base

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        session = self.Session()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

    async def startup(self) -> None:
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as e:
            raise RuntimeError("Database connection failed.") from e
        if self.automigrate:
            config = AlembicConfig(str(self.url.render_as_string(hide_password=False)))
            manager = AlembicManager(config)
            manager.apply_migrations()

    async def shutdown(self) -> None:
        await self.engine.dispose()
