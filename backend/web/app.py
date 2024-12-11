import os, time, json
from flask import Flask, Response, request, send_from_directory
from engine import vector_db, data_store, config, models, queryer

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


@app.route("/<data>/get/<id>", methods=["GET"])
def get_data_text(data, id):
    return {"text": vector_db.get_vector_text(data, [id])[0]}, 200


@app.route("/<data>/files/<filename>", methods=["GET"])
def download_file(data, filename):
    data_dir = os.path.abspath(os.path.join(config.data_base_dir, data))
    print(data_dir)
    return send_from_directory(data_dir, filename)


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


@app.route("/api_spec", methods=["GET"])
def get_api_specs():
    return models.get_api_specs(), 200


@app.route("/api_spec/<api_spec>", methods=["GET"])
def get_api_config(api_spec):
    return models.get_api_config(api_spec), 200


@app.route("/api_spec/<api_spec>", methods=["PUT"])
def update_api_config(api_spec):
    conf = request.get_json()
    models.update_api_config(api_spec, conf)
    queryer.setStale(api_spec)
    return "", 204


@app.route("/models", methods=["GET"])
def get_models():
    reload = request.args.get("reload", "false")
    return models.get_models(reload == "true"), 200


@app.route("/api/chat/config", methods=["GET"])
def config():
    return {"starterQuestions": None}


def generate():
    from mock_data import pre_events, messeges, post_events

    for event in pre_events:
        yield f"8:{json.dumps(event)}\n"
        time.sleep(0.2)
    for message in messeges:
        yield f'0:"{message}"\n'
        time.sleep(0.2)
    for event in post_events:
        yield f"8:{json.dumps(event)}\n"
        time.sleep(0.2)


@app.route("/api/chat", methods=["POST"])
def chat():
    return Response(generate(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
