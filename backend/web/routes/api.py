import time, json
from flask import Blueprint, Response

api = Blueprint("api", __name__)


@api.route("/chat/config", methods=["GET"])
def config():
    return {"starterQuestions": None}


def generate():
    from web.routes.mock_data import pre_events, messeges, post_events

    for event in pre_events:
        yield f"8:{json.dumps(event)}\n"
        time.sleep(0.2)
    for message in messeges:
        yield f'0:"{message}"\n'
        time.sleep(0.2)
    for event in post_events:
        yield f"8:{json.dumps(event)}\n"
        time.sleep(0.2)


@api.route("/chat", methods=["POST"])
def chat():
    return Response(generate(), mimetype="text/plain")
