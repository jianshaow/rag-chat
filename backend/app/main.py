import logging, os, uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.engine import config
from app.api import frontend_base_url, files_url_prefix
from app.api.routes import api_router, legacy_router

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

app.include_router(api_router, prefix="/api")
app.include_router(legacy_router, prefix="/legacy")

app.mount(
    files_url_prefix,
    StaticFiles(directory=config.get_data_base_path(), check_dir=False),
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
