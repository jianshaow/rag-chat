import json, time
from llama_index.core.chat_engine.types import StreamingAgentChatResponse
from fastapi.responses import StreamingResponse

from engine import events
from .frontend import extract_sources_data


class VercelStreamingResponse(StreamingResponse):

    TEXT_PREFIX = "0:"
    DATA_PREFIX = "8:"
    ERROR_PREFIX = "3:"

    def __init__(self, response: StreamingAgentChatResponse):
        super().__init__(VercelStreamingResponse.stream_generator(response))

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
    def stream_generator(cls, response: StreamingAgentChatResponse):
        from .mock_response import post_events

        messages = response.response_gen
        sources_data = extract_sources_data(response)

        for event in events.event_callback_handler.event_gen():
            event_response = event.to_response()
            if event_response:
                yield cls.to_data(event_response)
        for message in messages:
            yield cls.to_text(message)
            time.sleep(0.2)
        for event in post_events:
            yield cls.to_data(event)
        yield cls.to_data(sources_data)
