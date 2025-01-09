from fastapi import APIRouter

from .chat import chat_router
from .legacy import legacy_router

api_router = APIRouter()
api_router.include_router(chat_router, prefix="/chat")
