import os
from typing import Any, Callable, Coroutine, Dict, List, Union

import yaml
from llama_index.core.tools import BaseTool, RetrieverTool
from llama_index.core.vector_stores.types import MetadataFilters
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from pydantic import BaseModel, RootModel, TypeAdapter

from app.engine import indexes, setting


class MCPServer(BaseModel):
    starter_question: str


class LocalMCPServer(MCPServer):
    command: str
    args: List[str]


class RemoteMCPServer(MCPServer):
    url: str
    headers: dict[str, Any] | None


MCPServerUnion = TypeAdapter(Union[LocalMCPServer, RemoteMCPServer])


class MCPServers(RootModel[Dict[str, MCPServer]]):

    def __getitem__(self, key: str) -> MCPServer:
        return self.root[key]

    def get(self, key: str, default: Any = None) -> MCPServer | None:
        return self.root.get(key, default)

    def keys(self):
        return self.root.keys()

    def items(self):
        return self.root.items()

    def values(self):
        return self.root.values()

    def update(self, other: Dict[str, MCPServer]):
        for key, value in other.items():
            mcp_server = MCPServerUnion.validate_python(value)
            self.root[key] = mcp_server


__built_mcp_server = LocalMCPServer(
    command="python",
    args=["app/engine/calc_tools.py"],
    starter_question="What is (121 * 3) + (6 * 7)?",
)


__mcp_servers = MCPServers.model_validate({"calc_tools": __built_mcp_server})

mcp_servers_config_file = os.environ.get("MCP_SERVERS_CONFIG", "mcp/mcp_servers.yaml")

if mcp_servers_config_file and os.path.isfile(mcp_servers_config_file):
    with open(mcp_servers_config_file, "r", encoding="utf-8") as file:
        mcp_servers_from_file = yaml.safe_load(file)
        __mcp_servers.update(mcp_servers_from_file["mcp_servers"])


async def get_retriever_tools(filters: MetadataFilters):
    data_dir = setting.get_data_dir()
    index = indexes.get_index(data_dir)
    retriever_tool = RetrieverTool.from_defaults(
        index.as_retriever(filters=filters, verbose=True)
    )
    return [retriever_tool]


async def get_mcp_tools(*args, **kwargs):
    mcp_server = get_mcp_server()

    if isinstance(mcp_server, LocalMCPServer):
        mcp_client = BasicMCPClient(mcp_server.command, mcp_server.args)
    elif isinstance(mcp_server, RemoteMCPServer):
        mcp_client = BasicMCPClient(mcp_server.url, headers=mcp_server.headers)
    else:
        raise ValueError("No mcp server is set!")

    mcp_tool_spec = McpToolSpec(client=mcp_client)
    return await mcp_tool_spec.to_tool_list_async()


class ToolSetSpec(BaseModel):
    name: str
    get_tools: Callable[..., Coroutine[Any, Any, List[Union[BaseTool, Callable]]]]


__tool_sets = {
    "retriever": ToolSetSpec(name="retriever", get_tools=get_retriever_tools),
    "mcp_tools": ToolSetSpec(name="mcp_tools", get_tools=get_mcp_tools),
}


def get_tool_sets():
    return list(__tool_sets.keys())


def get_tool_set():
    return __tool_sets.get(setting.get_tool_set())


def get_mcp_servers():
    return list(__mcp_servers.keys())


def get_mcp_server():
    return __mcp_servers[setting.get_mcp_server()]


if __name__ == "__main__":
    import asyncio

    mcp_tools = asyncio.run(get_mcp_tools())
    for tool in mcp_tools:
        print(tool.metadata.name, ":", tool.metadata.description)
