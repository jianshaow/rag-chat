from fastapi import APIRouter

from .chat import chat_router
from .files import files_router
from .legacy import legacy_router

api_router = APIRouter()
api_router.include_router(chat_router, prefix="/chat")
api_router.include_router(files_router, prefix="/files")
