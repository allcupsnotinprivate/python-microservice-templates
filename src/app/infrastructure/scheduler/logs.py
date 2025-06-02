import time
from asyncio import iscoroutinefunction
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar, Union, cast

from loguru import logger

from app.utils.tokens import generate_prefixed_uuid

R = TypeVar("R")
A = TypeVar("A")


def wrap_with_log_context(
    job_id: str | None = None, job_name: str | None = None
) -> Callable[[Callable[..., Union[Awaitable[R], R]]], Callable[..., Union[Awaitable[R], R]]]:
    def decorator(func: Callable[..., Union[Awaitable[R], R]]) -> Callable[..., Union[Awaitable[R], R]]:
        is_async = iscoroutinefunction(func)

        if is_async:

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> R:
                context_id = generate_prefixed_uuid("job", 16)
                job_label = job_name or func.__name__

                with logger.contextualize(context_id=context_id, job_id=job_id, job_label=job_label):
                    with logger.catch(reraise=True):
                        logger.info("Started job.")
                        start_time = time.monotonic()
                        try:
                            result = await cast(Callable[..., Awaitable[R]], func)(*args, **kwargs)
                            return result
                        finally:
                            elapsed = time.monotonic() - start_time
                            logger.info("Finished job.", elapsed=f"{elapsed:.3f}")

            return async_wrapper
        else:

            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> R:
                context_id = generate_prefixed_uuid("job", 16)
                job_label = job_name or func.__name__

                with logger.contextualize(context_id=context_id, job_id=job_id, job_label=job_label):
                    with logger.catch(reraise=True):
                        logger.info("Started job.")
                        start_time = time.monotonic()
                        try:
                            return func(*args, **kwargs)  # type: ignore[return-value]
                        finally:
                            elapsed = time.monotonic() - start_time
                            logger.info("Finished job.", elapsed=f"{elapsed:.3f}")

            return sync_wrapper

    return decorator
