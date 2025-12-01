import logging
from typing import Any, Dict

from fastapi import APIRouter

from app.engine.tools import call_tool, get_mcp_servers, get_tool_sets

logger = logging.getLogger(__name__)

tools_router = r = APIRouter()


@r.get("", tags=["tools"])
def tool_sets():
    return get_tool_sets()


@r.get("/mcp_servers", tags=["tools"])
def mcp_servers():
    return get_mcp_servers()


@r.post("/{tool_name}", tags=["tools"])
async def run_tool(kwargs: Dict[str, Any]):
    return await call_tool(**kwargs)
