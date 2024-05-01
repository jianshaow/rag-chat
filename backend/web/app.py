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
    return data_store.get_all_data_path(), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
