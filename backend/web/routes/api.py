import time, json
from flask import Blueprint, Response, request, send_from_directory

from engine import models, queryer, config, backend_base_url

api = Blueprint("api", __name__)


@api.route("/chat/config", methods=["GET"])
def chat_config():
    return {"starterQuestions": None}


def generate(messages: models.ChatMessages):
    from web.routes.mock_response import pre_events, post_events

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
                            "url": backend_base_url
                            + "/api/en_novel/files/"
                            + node.node.metadata.get("file_name"),
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


@api.route("/<data>/files/<filename>", methods=["GET"])
def download_file(data, filename):
    data_dir = config.get_data_path(data)
    return send_from_directory(data_dir, filename)
