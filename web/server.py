from flask import Flask
from flask import request

from engine import data_store, config, queryer

app = Flask(__name__)


@app.route("/query", methods=["GET"])
def query_index():
    data_name = request.args.get("data", config.default_data_name)
    query_text = request.args.get("text", None)
    if query_text is None:
        return (
            "No text found, please include a ?text=blah parameter in the URL",
            400,
        )
    return queryer.query(data_name, query_text), 200


@app.route("/data", methods=["GET"])
def query_data():
    return data_store.get_all_data_path(), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
