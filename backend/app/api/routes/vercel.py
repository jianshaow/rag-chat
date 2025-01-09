import json
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
        event_callback_handler: events.EventCallbackHandler,
        messages: list[dict[str, str]],
        response: StreamingAgentChatResponse,
    ):
        super().__init__(
            self.__class__.stream_generator(event_callback_handler, messages, response)
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
    def stream_generator(
        cls,
        event_callback_handler: events.EventCallbackHandler,
        messages: list[dict[str, str]],
        response: StreamingAgentChatResponse,
    ):
        sources_data = extract_sources_data(response)
        yield cls.to_data(sources_data)

        for event in event_callback_handler.event_gen():
            event_response = event.to_response()
            if event_response:
                yield cls.to_data(event_response)

        final_response = ""
        for chunk in response.response_gen:
            final_response += chunk
            yield cls.to_text(chunk)

        yield cls.to_data(cls.next_questions(messages, final_response))

    @classmethod
    def next_questions(cls, messages: list[dict[str, str]], response: str):
        return {
            "type": "suggested_questions",
            "data": suggest_next_questions(messages, response),
        }
