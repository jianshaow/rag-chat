import base64
import binascii
import json
import logging

from fastapi import APIRouter, HTTPException, Request, Response

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
async def run_tool(tool_name: str, request: Request):
    args: dict = await request.json()
    result = await call_tool(tool_name, **args)
    return Response(content=result, media_type="text/plain")


@r.get("/{tool_name}", tags=["tools"])
async def run_tool_get(tool_name: str, tool_kwargs: str):
    try:
        decoded_tool_kwargs = base64.urlsafe_b64decode(tool_kwargs.encode("utf-8"))
        args = json.loads(decoded_tool_kwargs.decode("utf-8"))
    except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid tool_kwargs") from exc

    if not isinstance(args, dict):
        raise HTTPException(status_code=400, detail="tool_kwargs must decode to an object")

    result = await call_tool(tool_name, **args)
    return Response(content=result, media_type="text/plain")
