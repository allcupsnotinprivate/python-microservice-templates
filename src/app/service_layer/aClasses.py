import abc
import inspect
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from app.exceptions import ServiceError

T = TypeVar("T", bound=Callable[..., Any])


class ServiceMeta(abc.ABCMeta):
    def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> Any:
        for attr_name, attr_value in namespace.items():
            if inspect.iscoroutinefunction(attr_value) or inspect.isfunction(attr_value):
                namespace[attr_name] = mcs._wrap_with_exception_handler(attr_value)
        return super().__new__(mcs, name, bases, namespace)

    @staticmethod
    def _wrap_with_exception_handler(func: T) -> T:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return await func(*args, **kwargs)
                except ServiceError:
                    raise
                except Exception as e:
                    raise ServiceError(f"Unexpected error in {func.__name__}: {e}") from e

            return cast(T, async_wrapper)

        else:

            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return func(*args, **kwargs)
                except ServiceError:
                    raise
                except Exception as e:
                    raise ServiceError(f"Unexpected error in {func.__name__}: {e}") from e

            return cast(T, sync_wrapper)


class AService(metaclass=ServiceMeta):
    pass
