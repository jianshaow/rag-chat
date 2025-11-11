from contextvars import ContextVar
from typing import Callable, List, Union

from llama_index.core.tools import BaseTool, RetrieverTool
from llama_index.core.vector_stores.types import MetadataFilters
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from pydantic import BaseModel

from app.engine import events, indexes, setting


def get_retriever_tools(filters: MetadataFilters):
    data_dir = setting.get_data_dir()
    index, context = indexes.get_index(data_dir)
    retriever_tool = RetrieverTool.from_defaults(
        index.as_retriever(filters=filters, verbose=True)
    )
    return [retriever_tool], context


import asyncio


def get_mcp_tools(**kwargs):
    async def get_sse_tools_async():
        mcp_client = BasicMCPClient(setting.get_mcp_url())
        mcp_tool_spec = McpToolSpec(client=mcp_client)

        return await mcp_tool_spec.to_tool_list_async()

    return asyncio.run(get_sse_tools_async()), indexes.contextvar_event_handler.context


class ToolSetSpec(BaseModel):
    name: str
    get_tools: Callable[
        ...,
        tuple[
            List[Union[BaseTool, Callable]],
            ContextVar[events.QueueEventCallbackHandler],
        ],
    ]


__tool_sets = {
    "retriever": ToolSetSpec(name="retriever", get_tools=get_retriever_tools),
    "mcp_tools": ToolSetSpec(name="mcp_tools", get_tools=get_mcp_tools),
}


def get_tool_sets():
    return list(__tool_sets.keys())


def get_tool_set():
    return __tool_sets.get(setting.get_tool_set())
