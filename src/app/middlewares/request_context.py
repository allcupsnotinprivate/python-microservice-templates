from loguru import logger
from starlette.types import ASGIApp, Receive, Scope, Send

from app.utils.tokens import generate_prefixed_uuid


class RequestContextMiddleware:
    def __init__(self, app: ASGIApp, header_name: str = "X-Request-ID"):
        self.app = app
        self.header_name = header_name.lower()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            headers = dict(scope["headers"])
            raw_request_id = headers.get(self.header_name)
            request_id = raw_request_id if raw_request_id else generate_prefixed_uuid("http", length=16)

            with logger.contextualize(context_id=request_id):
                with logger.catch(reraise=True):
                    await self.app(scope, receive, send)

        else:
            await self.app(scope, receive, send)
