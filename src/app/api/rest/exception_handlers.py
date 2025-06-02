from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app import exceptions


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(exceptions.ServiceError)
    async def base_service_error_handler(request: Request, exc: exceptions.ServiceError) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": "ServiceError", "message": str(exc)},
        )
