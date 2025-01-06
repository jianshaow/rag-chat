import os
from flask import Flask, send_from_directory

from web.routes import api, legacy

frontend = os.path.abspath(os.path.join("../frontend", "out"))
frontend = os.environ.get("FRONTEND_DIR", frontend)

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(legacy, url_prefix="/legacy")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def main(path:str):
    if path == "" or path == "setting":
        return send_from_directory(frontend, "index.html")
    elif path.startswith("legacy"):
        return send_from_directory(frontend, "legacy.html")
    else:
        return send_from_directory(frontend, path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
