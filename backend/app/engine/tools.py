import asyncio
import os
from contextlib import AsyncExitStack
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Callable, Coroutine, Dict, List, Union
from urllib.parse import parse_qs, urlparse

import yaml
from llama_index.core.tools import BaseTool, RetrieverTool
from llama_index.core.tools.retriever_tool import DEFAULT_NAME
from llama_index.core.tools.types import AsyncBaseTool, ToolOutput
from llama_index.core.vector_stores.types import MetadataFilters
from llama_index.tools.mcp import McpToolSpec
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import CallToolResult, TextContent
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


@dataclass
class _OwnedMCPSession:
    session: ClientSession
    close_event: asyncio.Event
    owner_task: asyncio.Task[None]


class MCPSessionManager:
    def __init__(self, timeout: int = 120):
        self.timeout = timeout
        self._condition = asyncio.Condition()
        self._session: ClientSession | None = None
        self._owned_session: _OwnedMCPSession | None = None
        self._server_config: str | None = None
        self._replacing = False

    async def get_session(self, server: MCPServer) -> ClientSession:
        server_config = server.model_dump_json()
        async with self._condition:
            while self._replacing:
                await self._condition.wait()
            if self._session is not None and self._server_config == server_config:
                return self._session

            self._replacing = True

        new_owned_session: _OwnedMCPSession | None = None
        try:
            new_owned_session = await self._start_owned_session(server)
            old_owned_session = self._owned_session
            if old_owned_session is not None:
                await self._close_owned_session(old_owned_session)
        except BaseException:
            if new_owned_session is not None:
                await self._close_owned_session(new_owned_session)
            async with self._condition:
                self._replacing = False
                self._condition.notify_all()
            raise

        async with self._condition:
            if new_owned_session is None:
                raise RuntimeError("MCP session owner returned no session")
            self._owned_session = new_owned_session
            self._session = new_owned_session.session
            self._server_config = server_config
            self._replacing = False
            self._condition.notify_all()
            return new_owned_session.session

    async def close(self) -> None:
        async with self._condition:
            while self._replacing:
                await self._condition.wait()
            self._replacing = True

        try:
            if self._owned_session is not None:
                await self._close_owned_session(self._owned_session)
        finally:
            async with self._condition:
                self._session = None
                self._owned_session = None
                self._server_config = None
                self._replacing = False
                self._condition.notify_all()

    async def _start_owned_session(self, server: MCPServer) -> _OwnedMCPSession:
        ready: asyncio.Future[ClientSession] = (
            asyncio.get_running_loop().create_future()
        )
        close_event = asyncio.Event()
        owner_task = asyncio.create_task(
            self._run_session_owner(server, ready, close_event)
        )
        try:
            session = await ready
        except BaseException:
            close_event.set()
            await owner_task
            raise
        return _OwnedMCPSession(session, close_event, owner_task)

    async def _run_session_owner(
        self,
        server: MCPServer,
        ready: asyncio.Future[ClientSession],
        close_event: asyncio.Event,
    ) -> None:
        try:
            async with AsyncExitStack() as stack:
                session = await self._create_session(stack, server)
                ready.set_result(session)
                await close_event.wait()
        except BaseException as exc:
            if not ready.done():
                ready.set_exception(exc)
            raise

    @staticmethod
    async def _close_owned_session(owned_session: _OwnedMCPSession) -> None:
        owned_session.close_event.set()
        await owned_session.owner_task

    async def _create_session(
        self, stack: AsyncExitStack, server: MCPServer
    ) -> ClientSession:
        if isinstance(server, LocalMCPServer):
            streams = await stack.enter_async_context(
                stdio_client(
                    StdioServerParameters(command=server.command, args=server.args)
                )
            )
        elif isinstance(server, RemoteMCPServer):
            if self._uses_sse(server.url):
                streams = await stack.enter_async_context(
                    sse_client(server.url, headers=server.headers)
                )
            else:
                read, write, _ = await stack.enter_async_context(
                    streamablehttp_client(server.url, headers=server.headers)
                )
                streams = (read, write)
        else:
            raise ValueError(f"Unsupported MCP server type: {type(server).__name__}")

        session = await stack.enter_async_context(
            ClientSession(
                *streams,
                read_timeout_seconds=timedelta(seconds=self.timeout),
            )
        )
        await session.initialize()
        return session

    @staticmethod
    def _uses_sse(url: str) -> bool:
        parsed_url = urlparse(url)
        return (
            parsed_url.path.rstrip("/").endswith("/sse")
            or "/sse/" in parsed_url.path
            or parse_qs(parsed_url.query).get("transport") == ["sse"]
        )


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
__mcp_session_manager = MCPSessionManager(
    timeout=int(os.getenv("MCP_SESSION_TIMEOUT", "120"))
)

mcp_servers_config_file = os.environ.get("MCP_SERVERS_CONFIG", "mcp/mcp_servers.yaml")

if mcp_servers_config_file and os.path.isfile(mcp_servers_config_file):
    with open(mcp_servers_config_file, "r", encoding="utf-8") as file:
        mcp_servers_from_file = yaml.safe_load(file)
        __mcp_servers.update(mcp_servers_from_file["mcp_servers"])


async def get_retriever_tools(
    data_dir: str, filters: MetadataFilters
) -> Dict[str, BaseTool]:
    index = indexes.get_index(data_dir)
    retriever_tool = RetrieverTool.from_defaults(
        index.as_retriever(filters=filters, verbose=True)
    )
    return {DEFAULT_NAME: retriever_tool}


async def get_mcp_tools(*_args, **_kwargs) -> Dict[str, BaseTool]:
    mcp_server = get_mcp_server()
    mcp_session = await __mcp_session_manager.get_session(mcp_server)
    mcp_tool_spec = McpToolSpec(client=mcp_session)
    tools = await mcp_tool_spec.to_tool_list_async()
    return {tool.metadata.name: tool for tool in tools if tool.metadata.name}


class ToolSetSpec(BaseModel):
    name: str
    get_tools: Callable[..., Coroutine[Any, Any, Dict[str, BaseTool]]]


__tool_sets = {
    "retriever": ToolSetSpec(name="retriever", get_tools=get_retriever_tools),
    "mcp_tools": ToolSetSpec(name="mcp_tools", get_tools=get_mcp_tools),
}


def get_tool_sets():
    return list(__tool_sets.keys())


def get_tool_set():
    return __tool_sets.get(setting.get_tool_set())


async def get_tools(*args, **kwargs) -> Dict[str, BaseTool]:
    tool_set = get_tool_set()
    if tool_set:
        return await tool_set.get_tools(*args, **kwargs)
    return {}


async def get_tool(tool_name: str, *args, **kwargs) -> BaseTool | None:
    tools = await get_tools(*args, **kwargs)
    return tools.get(tool_name)


async def call_tool(tool_name: str, *args, **kwargs):
    _tool = await get_tool(tool_name)
    if _tool and isinstance(_tool, AsyncBaseTool):
        output: ToolOutput = await _tool.acall(*args, **kwargs)
        result: CallToolResult = output.raw_output
        text = "\n".join(
            [block.text for block in result.content if isinstance(block, TextContent)]
        )
        return text


def get_mcp_servers():
    return list(__mcp_servers.keys())


def get_mcp_server():
    return __mcp_servers[setting.get_mcp_server()]


async def replace_mcp_session(server_name: str) -> None:
    mcp_server = __mcp_servers.get(server_name)
    if mcp_server is None:
        raise ValueError(f"Unknown MCP server: {server_name}")
    await __mcp_session_manager.get_session(mcp_server)


async def close_mcp_session() -> None:
    await __mcp_session_manager.close()


if __name__ == "__main__":
    mcp_tools = asyncio.run(get_mcp_tools())
    for tool in mcp_tools.values():
        print("tool name:", tool.metadata.name)
        print("-" * 80)
        print(tool.metadata.name, ":", tool.metadata.description)
        print("=" * 80)
