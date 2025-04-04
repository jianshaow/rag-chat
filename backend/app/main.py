import logging
import logging.config
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app.api import files_url_prefix, frontend_base_url
from app.api.routes import api_router
from app.engine import events, indexes, setting

logging_conf = os.getenv("LOGGING_CONF", "logging.conf")
logging.config.fileConfig(logging_conf, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

frontend = os.path.abspath(os.path.join("../frontend", "out"))
frontend = os.getenv("FRONTEND_DIR", frontend)

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


app.mount(
    files_url_prefix,
    StaticFiles(directory=setting.get_data_base_dir(), check_dir=False),
    name="data_base_dir",
)


class FrontendStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        if path == "setting":
            file_path = os.path.join(frontend, "query", "index.html")
            return FileResponse(file_path)

        return await super().get_response(path, scope)


app.mount("/", FrontendStaticFiles(directory=frontend, html=True), name="frontend")


if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "8000"))

    uvicorn.run(app="app.main:app", host=app_host, port=app_port, reload=True)
