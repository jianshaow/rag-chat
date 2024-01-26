from flask import Flask
from flask import request

from engine import config, queryer

app = Flask(__name__)


@app.route("/query", methods=["GET"])
def query_index():
    query_text = request.args.get("text", None)
    if query_text is None:
        return (
            "No text found, please include a ?text=blah parameter in the URL",
            400,
        )
    return queryer.query(query_text), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
