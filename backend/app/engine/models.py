from typing import Any, Callable, Dict, Generic, Type, TypeVar

from google.genai import Client as GoogleClient
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.llms import LLM
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from ollama import Client as OllamaClient
from openai import OpenAI as OpenAIClient
from pydantic import BaseModel

from app.engine import (
    GOOGLE_CHAT_MODEL,
    GOOGLE_EMBED_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_CHAT_MODEL,
    OLLAMA_EMBED_MODEL,
    OLLAMA_HOST,
    OPENAI_CHAT_MODEL,
    OPENAI_EMBED_MODEL,
    caches,
    setting,
)

T = TypeVar("T", BaseEmbedding, LLM)


def openai_embed_models() -> list[str]:
    client = OpenAIClient()
    models = client.models.list()
    return [
        model.id
        for model in models
        if model.owned_by == "openai" and model.id.startswith("text-embedding")
    ]


def openai_chat_models() -> list[str]:
    client = OpenAIClient()
    models = client.models.list()
    return [
        model.id
        for model in models
        if model.owned_by == "openai" and not model.id.startswith("text-embedding")
    ]


def google_embed_models() -> list[str]:
    client = GoogleClient()
    models = client.models.list()
    return [
        model.name or ""
        for model in models
        if "embedContent" in model.supported_actions  # type: ignore
    ]


def google_chat_models() -> list[str]:
    client = GoogleClient()
    models = client.models.list()
    return [
        model.name or ""
        for model in models
        if "generateContent" in model.supported_actions  # type: ignore
    ]


def ollama_embed_models() -> list[str]:
    client = OllamaClient(OLLAMA_HOST)
    response = client.list()
    return [
        model.model
        for model in response.models
        if (model.details and model.details.family and "bert" in model.details.family)
    ]  # type: ignore


def ollama_chat_models() -> list[str]:
    client = OllamaClient(OLLAMA_HOST)
    response = client.list()
    return [
        model.model
        for model in response.models
        if (
            model.details is None
            or model.details.family is None
            or "bert" not in model.details.family
        )
    ]  # type: ignore


class ModelSpec(BaseModel, Generic[T]):
    model_class: Type[T]
    model_args: Dict[str, Any]
    models_func: Callable[[], list[str]]


__model_configs: Dict[str, Dict[str, ModelSpec]] = {
    "openai": {
        "embed": ModelSpec(
            model_class=OpenAIEmbedding,
            model_args={"model": OPENAI_EMBED_MODEL},
            models_func=openai_embed_models,
        ),
        "chat": ModelSpec(
            model_class=OpenAI,
            model_args={"model": OPENAI_CHAT_MODEL},
            models_func=openai_chat_models,
        ),
    },
    "google": {
        "embed": ModelSpec(
            model_class=GoogleGenAIEmbedding,
            model_args={"model": GOOGLE_EMBED_MODEL, "transport": "rest"},
            models_func=google_embed_models,
        ),
        "chat": ModelSpec(
            model_class=GoogleGenAI,
            model_args={"model": GOOGLE_CHAT_MODEL, "transport": "rest"},
            models_func=google_chat_models,
        ),
    },
    "ollama": {
        "embed": ModelSpec(
            model_class=OllamaEmbedding,
            model_args={
                "base_url": OLLAMA_BASE_URL,
                "model_name": OLLAMA_EMBED_MODEL,
            },
            models_func=ollama_embed_models,
        ),
        "chat": ModelSpec(
            model_class=Ollama,
            model_args={
                "base_url": OLLAMA_BASE_URL,
                "model": OLLAMA_CHAT_MODEL,
                "thinking": False,
            },
            models_func=ollama_chat_models,
        ),
    },
}


def get_model_providers() -> list[str]:
    import app.engine.extension as ext

    ext_model_providers = ext.get_model_providers()
    return list(__model_configs.keys()) + ext_model_providers


__model_lists: dict[str, dict[str, list[str]]] = {"embed": {}, "chat": {}}


def get_models(model_type: str, reload: bool) -> list[str]:
    model_provider = setting.get_model_provider()
    model_list = __model_lists[model_type].get(model_provider)
    if model_list is None or reload:
        model_config = __model_configs.get(model_provider)
        if model_config:
            model_list = model_config[model_type].models_func()
            __model_lists[model_type][model_provider] = model_list
        else:
            import app.engine.extension as ext

            model_list = ext.get_models(model_provider, model_type)
            __model_lists[model_type][model_provider] = model_list
    return model_list


def get_embed_model_name() -> str:
    return get_model_config(setting.get_model_provider()).embed_model


def get_escaped_embed_model_name() -> str:
    return get_embed_model_name().replace(":", "_").replace("/", "_")


def get_chat_model_name() -> str:
    return get_model_config(setting.get_model_provider()).chat_model


class ModelConfig(BaseModel):
    embed_model: str
    chat_model: str


def get_model_config(model_provider: str) -> ModelConfig:
    model_config = __model_configs.get(model_provider)
    if model_config:
        embed_model_args: dict = model_config["embed"].model_args
        embed_model = embed_model_args.get("model") or embed_model_args.get(
            "model_name", ""
        )
        chat_model = model_config["chat"].model_args["model"]
        return ModelConfig(embed_model=embed_model, chat_model=chat_model)
    else:
        import app.engine.extension as ext

        return ext.get_model_config(model_provider)


def update_model_config(model_provider: str, conf: ModelConfig):
    model_config = __model_configs.get(model_provider)
    if model_config:
        embed_model_args = model_config["embed"].model_args
        if "model" in embed_model_args:
            embed_model_args["model"] = conf.embed_model
        if "model_name" in embed_model_args:
            embed_model_args["model_name"] = conf.embed_model
        model_config["chat"].model_args["model"] = conf.chat_model
    else:
        import app.engine.extension as ext

        ext.update_model_config(model_provider, conf)


def new_model(model_type: str) -> Type[T]:
    model_provider = setting.get_model_provider()
    model_config = __model_configs.get(model_provider)
    if model_config:
        model_class = model_config[model_type].model_class
        model_args = model_config[model_type].model_args
        return model_class(**model_args)
    else:
        import app.engine.extension as ext

        return ext.new_model(model_provider, model_type)


def get_embed_model() -> BaseEmbedding:
    return caches.get_embed_model(lambda: new_model("embed"))


def get_chat_model() -> LLM:
    return caches.get_chat_model(lambda: new_model("chat"))


if __name__ == "__main__":
    print(__model_configs)
