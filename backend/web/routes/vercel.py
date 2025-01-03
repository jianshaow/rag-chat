import json, time
from llama_index.core.base.response.schema import StreamingResponse
from web.routes.fe_response import get_sources
from engine import events


def stream_gen(response: StreamingResponse):
    from web.routes.mock_response import post_events

    messages = response.response_gen
    sources = get_sources(response)

    for event in events.event_callback_handler.event_gen():
        yield f"8:{json.dumps([event.to_response()])}\n"
    for message in messages:
        yield f"0:{json.dumps(message)}\n"
        time.sleep(0.2)
    for event in post_events:
        yield f"8:{json.dumps(event)}\n"
    yield f"8:{sources}\n"
