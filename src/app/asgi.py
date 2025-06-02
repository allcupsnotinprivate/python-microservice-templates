import contextlib
from typing import AsyncIterator

from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi import FastAPI

from app import infrastructure
from app.api import add_exception_handlers, register_tasks
from app.api import router as root_router
from app.container import container


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with container:  # noqa: E117
        with container.sync_context() as ctx:
            database: infrastructure.APostgresDatabase = ctx.resolve(infrastructure.APostgresDatabase)
            scheduler: infrastructure.ASchedulerManager = ctx.resolve(infrastructure.ASchedulerManager)  # type: ignore[type-abstract]

        await database.startup()
        register_tasks(scheduler)
        scheduler.start(paused=False)
        yield
        scheduler.shutdown(wait=True)
        await database.shutdown()


def create_application() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(AioInjectMiddleware, container=container)  # noqa
    add_exception_handlers(app)

    app.include_router(root_router, prefix="/api")

    return app
