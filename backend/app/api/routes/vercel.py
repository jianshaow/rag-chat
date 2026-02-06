import json
import logging
from typing import AsyncGenerator, Awaitable, Callable, List, Tuple

from aiostream import stream
from fastapi.responses import StreamingResponse
from llama_index.core.agent.workflow import AgentStream, ToolCall, ToolCallResult
from llama_index.core.base.response.schema import AsyncStreamingResponse
from llama_index.core.chat_engine.types import StreamingAgentChatResponse
from llama_index.core.schema import NodeWithScore
from llama_index.core.tools.retriever_tool import DEFAULT_NAME
from mcp.types import CallToolResult
from workflows.handler import WorkflowHandler

from app.api.routes.payload import ChatMessages, SourceNode
from app.api.services.suggestion import suggest_next_questions
from app.engine.events import QueueEventCallbackHandler

logger = logging.getLogger(__name__)


class VercelStreamingResponse(StreamingResponse):

    TEXT_PREFIX = "0:"
    DATA_PREFIX = "8:"
    ERROR_PREFIX = "3:"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_chat_response(
        cls,
        response: Awaitable[StreamingAgentChatResponse],
        event_handler: QueueEventCallbackHandler,
        messages: ChatMessages | None = None,
    ):
        async def await_response():
            result = await response
            return result.source_nodes, result.async_response_gen()

        response_generator = cls.response_generator(
            await_response, event_handler, messages
        )
        event_generator = cls.event_generator(event_handler)
        stream_generator = cls.merge_generator(
            response_generator, event_generator, event_handler
        )
        return cls(stream_generator)

    @classmethod
    def from_query_response(
        cls,
        response: Awaitable[AsyncStreamingResponse],
        event_handler: QueueEventCallbackHandler,
        messages: ChatMessages | None = None,
    ):
        async def await_response():
            result = await response
            return result.source_nodes, result.async_response_gen()

        response_generator = cls.response_generator(
            await_response, event_handler, messages
        )
        event_generator = cls.event_generator(event_handler)

        stream_generator = cls.merge_generator(
            response_generator, event_generator, event_handler
        )
        return cls(stream_generator)

    @classmethod
    def from_agent_response(
        cls,
        response: WorkflowHandler,
        messages: ChatMessages | None = None,
        **kwargs,
    ):
        response_generator = cls.agent_event_generator(response, messages)
        return cls(response_generator, **kwargs)

    @classmethod
    async def response_generator(
        cls,
        await_response: Callable[
            [], Awaitable[Tuple[List[NodeWithScore], AsyncGenerator]]
        ],
        event_handler: QueueEventCallbackHandler,
        messages: ChatMessages | None = None,
    ):
        source_nodes, response_gen = await await_response()
        yield cls.to_sources_data(SourceNode.from_source_nodes(source_nodes))

        final_response = ""
        async for chunk in response_gen:
            final_response += chunk
            yield cls.to_text(chunk)

        if messages:
            yield await cls.to_suggested_questions_data(messages, final_response)

        event_handler.is_done = True

    @classmethod
    async def event_generator(cls, event_callback_handler: QueueEventCallbackHandler):
        async for event in event_callback_handler.async_event_gen():
            event_response = event.to_response()
            if event_response:
                yield cls.to_data(event_response)

    @classmethod
    async def merge_generator(
        cls,
        response_generator: AsyncGenerator[str, None],
        event_generator: AsyncGenerator[str, None],
        event_handler: QueueEventCallbackHandler,
    ):
        event_handler.is_done = False
        combine = stream.merge(response_generator, event_generator)
        is_stream_started = False
        try:
            async with combine.stream() as streamer:
                async for output in streamer:
                    if not is_stream_started:
                        is_stream_started = True
                        yield cls.to_text("")
                    yield output
        except Exception as e:  # pylint: disable=broad-except
            logger.error(e, exc_info=True)
            yield cls.to_error(
                "An unexpected error occurred while processing your request, preventing the creation of a final answer. Please try again."
            )
        finally:
            event_handler.is_done = True

    @classmethod
    async def agent_event_generator(
        cls, response: WorkflowHandler, messages: ChatMessages | None
    ):
        final_response = ""
        text_started = False
        async for event in response.stream_events():
            if isinstance(event, AgentStream):
                if not text_started:
                    text_started = True
                    yield cls.to_text_start()
                final_response = event.response
                yield cls.to_text(event.delta)
            elif isinstance(event, ToolCall):
                if text_started:
                    text_started = False
                    yield cls.to_text_end()
                if event.tool_name == DEFAULT_NAME:
                    title = f"Retrieving context for query: '{event.tool_kwargs}'"
                else:
                    title = f"Calling tool: '{event.tool_name}' with args: '{event.tool_kwargs}'"
                yield cls.to_event_data(title)
            elif isinstance(event, ToolCallResult):
                if text_started:
                    text_started = False
                    yield cls.to_text_end()
                raw_output = event.tool_output.raw_output
                if isinstance(raw_output, List):
                    yield cls.to_sources_data(SourceNode.from_source_nodes(raw_output))
                    title = f"Retrieved {len(raw_output)} sources to use as context for the query"
                elif isinstance(raw_output, CallToolResult):
                    yield cls.to_sources_data(
                        SourceNode.from_call_tool_result(
                            raw_output,
                            event.tool_id,
                            event.tool_name,
                            event.tool_kwargs,
                        )
                    )
                    title = f"Tool '{event.tool_name}' returned: {len(raw_output.content)} sources"
                else:
                    title = f"Tool '{event.tool_name}' returned"
                yield cls.to_event_data(title)
            else:
                if text_started:
                    text_started = False
                    yield cls.to_text_end()
                logger.debug("Unhandled event: %s", event.__class__)
        if messages:
            yield await cls.to_suggested_questions_data(messages, final_response)

    @classmethod
    def to_event_data(cls, title: str):
        event_data = {"type": "data-event", "data": {"title": title}}
        return cls.to_data(event_data)

    @classmethod
    def to_sources_data(cls, source_nodes: List[SourceNode]):
        sources_data = {
            "type": "data-sources",
            "data": {
                "nodes": [source_node.model_dump() for source_node in source_nodes]
            },
        }
        return cls.to_data(sources_data)

    @classmethod
    async def to_suggested_questions_data(cls, messages: ChatMessages, response: str):
        return cls.to_data(
            {
                "type": "data-suggested_questions",
                "data": await suggest_next_questions(messages.chat_messages, response),
            }
        )

    @classmethod
    def to_text_start(cls):
        return f"data: {json.dumps({'type':'text-start','id':'0'})}\n\n"

    @classmethod
    def to_text_end(cls):
        return f"data: {json.dumps({'type':'text-end','id':'0'})}\n\n"

    @classmethod
    def to_text(cls, token: str):
        return f"data: {json.dumps({'type':'text-delta','id':'0','delta':token})}\n\n"

    @classmethod
    def to_data(cls, data: dict):
        data_str = json.dumps(data)
        return f"data: {data_str}\n\n"

    @classmethod
    def to_error(cls, error: str):
        error_str = json.dumps(error)
        return f"data: {error_str}\n\n"
