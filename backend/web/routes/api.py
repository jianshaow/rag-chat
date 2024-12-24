import time, json
from flask import Blueprint, Response, request

from engine import models, queryer

api = Blueprint("api", __name__)


@api.route("/chat/config", methods=["GET"])
def config():
    return {"starterQuestions": None}


def generate(messages: models.ChatMessages):
    from web.routes.mock_data import pre_events, post_events

    response = queryer.stream_query("en_novel", messages)
    messages = response.response_gen
    sources = json.dumps(
        [
            {
                "type": "sources",
                "data": {
                    "nodes": [
                        {
                            "id": node.node_id,
                            "metadata": node.node.metadata,
                            "score": node.score,
                            "text": node.text,
                            "url": node.node.metadata.get("file_name"),
                        }
                        for node in response.source_nodes
                    ]
                },
            }
        ]
    )

    for event in pre_events:
        yield f"8:{json.dumps(event)}\n"
        time.sleep(0.2)
    for message in messages:
        yield f"0:{json.dumps(message)}\n"
        time.sleep(0.2)
    for event in post_events:
        yield f"8:{json.dumps(event)}\n"
    yield f"8:{sources}\n"


@api.route("/chat", methods=["POST"])
def chat():
    messages = request.json["messages"]
    chat_messages = models.ChatMessages(messages)
    return Response(generate(chat_messages), mimetype="text/plain")
