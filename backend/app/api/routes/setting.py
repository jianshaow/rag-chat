from fastapi import APIRouter, Request, status

from app.engine import setting

setting_router = r = APIRouter()


@r.get("", tags=["setting"])
def get_config():
    return setting.get_config()


@r.put("", tags=["setting"], status_code=status.HTTP_204_NO_CONTENT)
async def update_config(request: Request):
    conf = await request.json()
    setting.update_config(conf)
