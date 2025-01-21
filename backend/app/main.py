import logging
import logging.config
import os

import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import files_url_prefix, frontend_base_url
from app.api.routes import api_router, legacy_router
from app.engine import config, events, indexes

with open("logging.yaml", "r", encoding="utf-8") as file:
    conf = yaml.safe_load(file)
logging.config.dictConfig(conf)

logger = logging.getLogger(__name__)

frontend = os.path.abspath(os.path.join("../frontend", "out"))
frontend = os.environ.get("FRONTEND_DIR", frontend)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_base_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_handler_context(request, call_next):
    eventhandler = events.QueueEventCallbackHandler()
    context = indexes.contextvar_event_handler.context
    token = context.set(eventhandler)
    try:
        response = await call_next(request)
    finally:
        context.reset(token)
    return response


app.include_router(api_router, prefix="/api")
app.include_router(legacy_router, prefix="/legacy")

app.mount(
    files_url_prefix,
    StaticFiles(directory=config.get_data_base_dir(), check_dir=False),
    name="data_base_dir",
)
if os.path.exists(frontend):
    app.mount(
        "/",
        StaticFiles(directory=frontend, check_dir=False, html=True),
        name="frontend",
    )
else:
    logger.warning(
        "Frontend directory %s does not exist. Please build the frontend first if needed.",
        frontend,
    )


if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "8000"))

    uvicorn.run(app="app.main:app", host=app_host, port=app_port, reload=True)
