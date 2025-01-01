import json, time
from llama_index.core.base.response.schema import StreamingResponse
from web.routes.fe_response import get_sources


def stream_gen(response: StreamingResponse):
    from web.routes.mock_response import pre_events, post_events

    messages = response.response_gen
    sources = get_sources(response)

    for event in pre_events:
        yield f"8:{json.dumps(event)}\n"
        time.sleep(0.2)
    for message in messages:
        yield f"0:{json.dumps(message)}\n"
        time.sleep(0.2)
    for event in post_events:
        yield f"8:{json.dumps(event)}\n"
    yield f"8:{sources}\n"
