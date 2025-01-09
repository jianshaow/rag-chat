from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.engine import config

files_router = r = APIRouter()


@r.get("/{data}/{filename}", tags=["files"])
def download_file(data, filename):
    path = config.get_data_file(data, filename)
    return FileResponse(path=path)
