from fastapi import APIRouter

from .chat import chat_router
from .data import data_router
from .model import model_router
from .query import query_router
from .setting import setting_router
from .tools import tools_router

api_router = APIRouter()
api_router.include_router(query_router, prefix="/query")
api_router.include_router(chat_router, prefix="/chat")
api_router.include_router(data_router, prefix="/data")
api_router.include_router(model_router, prefix="/model")
api_router.include_router(setting_router, prefix="/setting")
api_router.include_router(tools_router, prefix="/tools")
