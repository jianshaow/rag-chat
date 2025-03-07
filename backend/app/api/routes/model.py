import logging

from fastapi import APIRouter, status

from app.engine import caches, models

logger = logging.getLogger(__name__)

model_router = r = APIRouter()


@r.get("/provider", tags=["model"])
async def get_model_providers() -> list[str]:
    return models.get_model_providers()


@r.get("/provider/{model_provider}", tags=["model"])
async def get_model_config(model_provider) -> models.ModelConfig:
    return models.get_model_config(model_provider)


@r.put(
    "/provider/{model_provider}", tags=["model"], status_code=status.HTTP_204_NO_CONTENT
)
async def update_model_config(model_provider, conf: models.ModelConfig):
    models.update_model_config(model_provider, conf)
    caches.invalidate(model_provider)


@r.get("/embed", tags=["model"])
async def get_embed_models(reload)-> list[str]:
    return models.get_models("embed", reload == "true")


@r.get("/chat", tags=["model"])
async def get_chat_models(reload)-> list[str]:
    return models.get_models("chat", reload == "true")
