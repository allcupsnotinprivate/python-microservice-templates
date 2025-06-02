from fastapi import APIRouter

from .exception_handlers import add_exception_handlers
from .v1 import router as v1_router

router = APIRouter()
router.include_router(v1_router, prefix="/v1")

__all__ = ["router", "add_exception_handlers"]
