from fastapi import APIRouter, Request, status

from app.engine import config

setting_router = r = APIRouter()


@r.get("", tags=["setting"])
def get_config():
    return config.get_config()


@r.put("", tags=["setting"], status_code=status.HTTP_204_NO_CONTENT)
async def update_config(request: Request):
    conf = await request.json()
    config.update_config(conf)
