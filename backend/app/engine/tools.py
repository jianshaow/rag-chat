from typing import Any, Callable, Coroutine, List, Union

from llama_index.core.tools import BaseTool, RetrieverTool
from llama_index.core.vector_stores.types import MetadataFilters
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from pydantic import BaseModel

from app.engine import indexes, setting


async def get_retriever_tools(filters: MetadataFilters):
    data_dir = setting.get_data_dir()
    index = indexes.get_index(data_dir)
    retriever_tool = RetrieverTool.from_defaults(
        index.as_retriever(filters=filters, verbose=True)
    )
    return [retriever_tool]


async def get_mcp_tools(*args, **kwargs):
    mcp_client = BasicMCPClient(setting.get_mcp_url())
    mcp_tool_spec = McpToolSpec(client=mcp_client)
    return await mcp_tool_spec.to_tool_list_async()


class ToolSetSpec(BaseModel):
    name: str
    get_tools: Callable[
        ...,
        Coroutine[
            Any,
            Any,
            List[Union[BaseTool, Callable]],
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
