import os
from flask import Blueprint, request, send_from_directory
from engine import vector_db, data_store, config, models, queryer

legacy = Blueprint("legacy", __name__)


@legacy.route("/<data>/query", methods=["POST"])
def query_index(data):
    raw_data = request.get_data()
    query = raw_data.decode("utf-8")
    return queryer.query(data, query), 200


@legacy.route("/<data>/get/<id>", methods=["GET"])
def get_data_text(data, id):
    return {"text": vector_db.get_vector_text(data, [id])[0]}, 200


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


@legacy.route("/api_spec", methods=["GET"])
def get_api_specs():
    return models.get_api_specs(), 200


@legacy.route("/api_spec/<api_spec>", methods=["GET"])
def get_api_config(api_spec):
    return models.get_api_config(api_spec), 200


@legacy.route("/api_spec/<api_spec>", methods=["PUT"])
def update_api_config(api_spec):
    conf = request.get_json()
    models.update_api_config(api_spec, conf)
    queryer.setStale(api_spec)
    return "", 204


@legacy.route("/embed_models", methods=["GET"])
def get_embed_models():
    reload = request.args.get("reload", "false")
    return models.get_models("embed", reload == "true"), 200


@legacy.route("/chat_models", methods=["GET"])
def get_chat_models():
    reload = request.args.get("reload", "false")
    return models.get_models("chat", reload == "true"), 200
