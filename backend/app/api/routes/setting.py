from fastapi import APIRouter, status

from app.engine import setting
from app.engine.setting import Setting

setting_router = r = APIRouter()


@r.get("", tags=["setting"])
async def get_config() -> Setting:
    return setting.get_config()


@r.put("", tags=["setting"], status_code=status.HTTP_204_NO_CONTENT)
async def update_config(new_setting: Setting):
    setting.update_config(new_setting)
