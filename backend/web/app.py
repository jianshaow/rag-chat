import os
from flask import Flask, request, send_from_directory
from engine import data_store, config, queryer

frontend = os.path.abspath(os.path.join("../frontend", "build"))
frontend = os.environ.get("FRONTEND_DIR", frontend)
static_folder = os.path.join(frontend, "static")

app = Flask(__name__, static_folder=static_folder)


@app.route("/", defaults={"path": ""})
@app.route("/<path>")
def main(path):
    if path == "" or path == "setting":
        return send_from_directory(frontend, "index.html")
    else:
        return send_from_directory(frontend, path)


@app.route("/<data>/query", methods=["POST"])
def query_index(data):
    raw_data = request.get_data()
    query = raw_data.decode("utf-8")
    return queryer.query(data, query), 200


@app.route("/data", methods=["GET"])
def query_data():
    return data_store.get_data_names(), 200


@app.route("/data_config", methods=["GET"])
def get_data_config():
    return data_store.get_data_config(), 200


@app.route("/data_config", methods=["PUT"])
def update_data_config():
    data_config = request.get_json()
    data_store.update_data_config(data_config)
    return "", 204


@app.route("/config", methods=["GET"])
def get_config():
    return config.get_config(), 200


@app.route("/config", methods=["PUT"])
def update_config():
    conf = request.get_json()
    config.update_config(conf)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
