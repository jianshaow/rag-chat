from typing import Type

from app.engine.models import T


def get_model_providers() -> list[str]:
    return []


def get_model_config(model_provider: str) -> dict[str, str]:
    raise NotImplementedError(f"model provider '{model_provider}' is not implemented")


def update_model_config(model_provider: str, conf: dict):
    raise NotImplementedError(f"model provider '{model_provider}' is not implemented")


def get_models(model_provider: str, model_type: str) -> list:
    raise NotImplementedError(
        f"'{model_type}' on model provider  '{model_provider}' is not implemented"
    )


def new_model(model_provider, model_type) -> Type[T]:
    raise NotImplementedError(
        f"Model type '{model_type}' on model provider '{model_provider}' is not implemented"
    )
