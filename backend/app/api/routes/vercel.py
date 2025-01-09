import json
from aiostream import stream
from typing import Awaitable
from llama_index.core.chat_engine.types import StreamingAgentChatResponse
from fastapi.responses import StreamingResponse

from app.engine import events
from app.api.services.suggestion import suggest_next_questions
from .frontend import extract_sources_data


class VercelStreamingResponse(StreamingResponse):

    TEXT_PREFIX = "0:"
    DATA_PREFIX = "8:"
    ERROR_PREFIX = "3:"

    def __init__(
        self,
        event_handler: events.EventCallbackHandler,
        messages: list[dict[str, str]],
        response: Awaitable[StreamingAgentChatResponse],
    ):
        super().__init__(
            self.__class__.stream_generator(event_handler, messages, response)
        )

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
        event_handler: events.EventCallbackHandler,
        messages: list[dict[str, str]],
        response: Awaitable[StreamingAgentChatResponse],
    ):
        event_handler.is_done = False
        response_generator = cls.response_generator(messages, response, event_handler)
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
        except Exception as e:
            print(e)
            yield cls.to_error(
                "An unexpected error occurred while processing your request, preventing the creation of a final answer. Please try again."
            )
        finally:
            event_handler.is_done = True

    @classmethod
    async def event_generator(cls, event_callback_handler: events.EventCallbackHandler):
        async for event in event_callback_handler.async_event_gen():
            event_response = event.to_response()
            if event_response:
                yield cls.to_data(event_response)

    @classmethod
    async def response_generator(
        cls,
        messages: list[dict[str, str]],
        response: Awaitable[StreamingAgentChatResponse],
        event_handler: events.EventCallbackHandler,
    ):
        result = await response

        sources_data = extract_sources_data(result)
        yield cls.to_data(sources_data)

        final_response = ""
        async for chunk in result.async_response_gen():
            final_response += chunk
            yield cls.to_text(chunk)

        yield cls.to_data(cls.next_questions(messages, final_response))

        event_handler.is_done = True

    @classmethod
    def next_questions(cls, messages: list[dict[str, str]], response: str):
        return {
            "type": "suggested_questions",
            "data": suggest_next_questions(messages, response),
        }
