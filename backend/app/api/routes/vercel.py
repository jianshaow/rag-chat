import json
import logging
from typing import AsyncGenerator, Awaitable, Callable, List, Tuple

from aiostream import stream
from fastapi.responses import StreamingResponse
from llama_index.core.chat_engine.types import StreamingAgentChatResponse
from llama_index.core.schema import NodeWithScore

from app.api import files_base_url
from app.api.routes.payload import ChatMessages
from app.api.services.suggestion import suggest_next_questions
from app.engine import events

logger = logging.getLogger(__name__)


class VercelStreamingResponse(StreamingResponse):

    TEXT_PREFIX = "0:"
    DATA_PREFIX = "8:"
    ERROR_PREFIX = "3:"

    def __init__(
        self,
        await_response: Callable[
            [], Awaitable[Tuple[List[NodeWithScore], AsyncGenerator]]
        ],
        event_handler: events.QueueEventCallbackHandler,
        messages: ChatMessages | None = None,
    ):
        super().__init__(
            self.__class__.stream_generator(
                await_response,
                event_handler,
                messages,
            ),
        )

    @classmethod
    def from_chat_response(
        cls,
        response: Awaitable[StreamingAgentChatResponse],
        event_handler: events.QueueEventCallbackHandler,
        messages: ChatMessages | None = None,
    ):
        async def await_response():
            result = await response
            return result.source_nodes, result.async_response_gen()

        return cls(await_response, event_handler, messages)

    @classmethod
    def to_text(cls, token: str):
        token = json.dumps(token)
        return f"{cls.TEXT_PREFIX}{token}\n"

    @classmethod
    def to_data(cls, data: dict):
        data_str = json.dumps(data)
        return f"{cls.DATA_PREFIX}[{data_str}]\n"

    @classmethod
    def to_error(cls, error: str):
        error_str = json.dumps(error)
        return f"{cls.ERROR_PREFIX}{error_str}\n"

    @classmethod
    async def stream_generator(
        cls,
        await_response: Callable[
            [], Awaitable[Tuple[List[NodeWithScore], AsyncGenerator]]
        ],
        event_handler: events.QueueEventCallbackHandler,
        messages: ChatMessages | None = None,
    ):
        event_handler.is_done = False
        response_generator = cls.response_generator(
            await_response, event_handler, messages
        )
        event_generator = cls.event_generator(event_handler)
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
    async def event_generator(
        cls, event_callback_handler: events.QueueEventCallbackHandler
    ):
        async for event in event_callback_handler.async_event_gen():
            event_response = event.to_response()
            if event_response:
                yield cls.to_data(event_response)

    @classmethod
    async def response_generator(
        cls,
        await_response: Callable[
            [], Awaitable[Tuple[List[NodeWithScore], AsyncGenerator]]
        ],
        event_handler: events.QueueEventCallbackHandler,
        messages: ChatMessages | None = None,
    ):
        source_nodes, response_gen = await await_response()
        yield cls.extract_sources_data(source_nodes)

        final_response = ""
        async for chunk in response_gen:
            final_response += chunk
            yield cls.to_text(chunk)

        if messages:
            yield await cls.next_questions_data(messages, final_response)

        event_handler.is_done = True

    @classmethod
    def extract_sources_data(cls, source_nodes: List[NodeWithScore]):
        sources_data = {
            "type": "sources",
            "data": {
                "nodes": [
                    cls._to_node_dict(source_node) for source_node in source_nodes
                ]
            },
        }
        return cls.to_data(sources_data)

    @classmethod
    def _to_node_dict(cls, source_node: NodeWithScore):
        data_dir = source_node.metadata.get("data_dir")
        file_name = source_node.metadata.get("file_name")
        url = f"{files_base_url}/{data_dir}/{file_name}"

        return {
            "id": source_node.node_id,
            "metadata": source_node.metadata,
            "score": source_node.score,
            "text": source_node.text,
            "url": url,
        }

    @classmethod
    async def next_questions_data(cls, messages: ChatMessages, response: str):
        return cls.to_data(
            {
                "type": "suggested_questions",
                "data": await suggest_next_questions(messages.chat_messages, response),
            }
        )
