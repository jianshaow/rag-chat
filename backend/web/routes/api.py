import time, json
from flask import Blueprint, Response, request

from engine import vector_db, data_store, config, models, queryer

api = Blueprint("api", __name__)


@api.route("/chat/config", methods=["GET"])
def config():
    return {"starterQuestions": None}


def generate(messages: models.ChatMessages):
    from web.routes.mock_data import pre_events, post_events

    messages = queryer.stream_query("en_novel", messages)

    for event in pre_events:
        yield f"8:{json.dumps(event)}\n"
        time.sleep(0.2)
    for message in messages:
        yield f'0:"{message}"\n'
    for event in post_events:
        yield f"8:{json.dumps(event)}\n"
        time.sleep(0.2)


@api.route("/chat", methods=["POST"])
def chat():
    messages = request.json["messages"]
    chat_messages = models.ChatMessages(messages)
    return Response(generate(chat_messages), mimetype="text/plain")
