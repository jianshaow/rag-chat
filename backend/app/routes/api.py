from flask import Blueprint, Response, request, send_from_directory

from engine import chatter, models, config
from web.routes.vercel import stream_gen

api = Blueprint("api", __name__)


@api.route("/chat/config", methods=["GET"])
def chat_config():
    return {"starterQuestions": None}


@api.route("/chat", methods=["POST"])
def chat():
    messages = request.json["messages"]  # type: ignore
    chat_messages = models.ChatMessages(messages)
    response = chatter.chat("en_novel", chat_messages)
    return Response(stream_gen(response), mimetype="text/plain")


@api.route("/<data>/files/<filename>", methods=["GET"])
def download_file(data, filename):
    data_dir = config.get_data_path(data)
    return send_from_directory(data_dir, filename)
