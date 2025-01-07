import os
from flask import Blueprint, request, send_from_directory
from engine import vector_db, data_store, config, models, queryer, chatter

legacy = Blueprint("legacy", __name__)


@legacy.route("/<data>/query", methods=["POST"])
def query_index(data):
    raw_data = request.get_data()
    query = raw_data.decode("utf-8")
    return queryer.query(data, query), 200


@legacy.route("/<data>/get/<id>", methods=["GET"])
def get_data_text(data, id):
    vector_texts = vector_db.get_vector_text(data, [id])
    text = vector_texts[0] if vector_texts else ""
    return {"text": text}, 200


@legacy.route("/<data>/files/<filename>", methods=["GET"])
def download_file(data, filename):
    data_dir = os.path.abspath(os.path.join(config.data_base_dir, data))
    print(data_dir)
    return send_from_directory(data_dir, filename)


@legacy.route("/data", methods=["GET"])
def query_data():
    return data_store.get_data_names(), 200


@legacy.route("/data_config", methods=["GET"])
def get_data_config():
    return data_store.get_data_config(), 200


@legacy.route("/data_config", methods=["PUT"])
def update_data_config():
    data_config = request.get_json()
    data_store.update_data_config(data_config)
    return "", 204


@legacy.route("/config", methods=["GET"])
def get_config():
    return config.get_config(), 200


@legacy.route("/config", methods=["PUT"])
def update_config():
    conf = request.get_json()
    config.update_config(conf)
    return "", 204


@legacy.route("/model_provider", methods=["GET"])
def get_model_providers():
    return models.get_model_providers(), 200


@legacy.route("/model_provider/<model_provider>", methods=["GET"])
def get_model_config(model_provider):
    return models.get_model_config(model_provider), 200


@legacy.route("/model_provider/<model_provider>", methods=["PUT"])
def update_model_config(model_provider):
    conf = request.get_json()
    models.update_model_config(model_provider, conf)
    queryer.setStale(model_provider)
    chatter.setStale(model_provider)
    return "", 204


@legacy.route("/embed_models", methods=["GET"])
def get_embed_models():
    reload = request.args.get("reload", "false")
    return models.get_models("embed", reload == "true"), 200


@legacy.route("/chat_models", methods=["GET"])
def get_chat_models():
    reload = request.args.get("reload", "false")
    return models.get_models("chat", reload == "true"), 200
