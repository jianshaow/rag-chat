import logging

from fastapi import APIRouter

from app.engine.tools import get_tool_sets

logger = logging.getLogger(__name__)

tools_router = r = APIRouter()


@r.get("", tags=["tools"])
def tool_sets():
    return get_tool_sets()
