import logging
import sys
from typing import Any, Dict, Final, Iterator, TypeGuard

from loguru import logger

from .types import LogLevel

logging_format: Final[str] = (
    " <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
    " | <level>{level: <8}</level>"
    " | PID:<cyan>{process.id}</cyan>"
    " | {extra[context_id]: <16}"
    " | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
    " | {message} <yellow>{extra_formatted}</yellow>"
)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_back and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def _patch_context(record: dict[str, Any]) -> None:
    if not record.get("context_id"):
        record["context_id"] = None


def is_dict_of_str_any(value: Any) -> TypeGuard[dict[str, Any]]:
    return isinstance(value, dict)


def _format_extra(record: Dict[str, Any]) -> None:
    extra = record.get("extra")
    if not is_dict_of_str_any(extra):
        record["extra_formatted"] = ""
        return

    def filter_context_id(item: tuple[str, Any]) -> bool:
        return item[0] != "context_id"

    filtered_extra: Iterator[tuple[str, Any]] = filter(filter_context_id, extra.items())
    record["extra_formatted"] = ", ".join(f"{key}={value}" for key, value in filtered_extra)


def patch(record: dict[str, Any]) -> None:
    _format_extra(record)
    _patch_context(record)


def configure_logger(
    enabled: bool,
    log_level: LogLevel,
) -> None:
    logger.remove()
    logger.configure(
        patcher=patch,  # type: ignore[arg-type] # noqa
        extra={
            "context_id": "None",
        },
    )

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    handler = InterceptHandler()

    logging.basicConfig(handlers=[], level=log_level.value)

    if enabled:
        logger.add(sys.stdout, format=logging_format, level=log_level.value, enqueue=True, serialize=False)

    loggers = (
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
        "asyncio",
        "starlette",
    )

    for logger_name in loggers:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers.clear()
        logging_logger.addHandler(handler)
        logging_logger.propagate = False
