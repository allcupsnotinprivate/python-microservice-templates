from fastapi import APIRouter

from .conversations import router as conversations_router

router = APIRouter()
router.include_router(conversations_router, tags=["Conversations"])

__all__ = ["router"]
