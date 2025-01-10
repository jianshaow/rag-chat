from openai import OpenAI as OriginalOpenAI
import google.generativeai as genai
import ollama

from llama_index.core.llms import LLM
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini
from llama_index.llms.ollama import Ollama

from . import (
    config,
    caches,
    ollama_host,
    ollama_base_url,
    ollama_embed_model,
    ollama_chat_model,
    openai_embed_model,
    openai_chat_model,
    gemini_embed_model,
    gemini_chat_model,
)


class NormOllamaEmbedding(OllamaEmbedding):

    def get_general_text_embedding(self, texts: str) -> list[float]:
        """Get Ollama embedding."""
        result = self._client.embed(
            model=self.model_name, input=texts, options=self.ollama_additional_kwargs
        )
        return result["embeddings"][0]

    async def aget_general_text_embedding(self, prompt: str) -> list[float]:
        """Asynchronously get Ollama embedding."""
        result = await self._async_client.embed(
            model=self.model_name, input=prompt, options=self.ollama_additional_kwargs
        )
        return result["embeddings"][0]


def openai_embed_models() -> list[str]:
    client = OriginalOpenAI()
    response = client.models.list()
    return [
        model.model_dump()["root"]
        for model in response.data
        if str(model.model_dump()["root"]).startswith("text-embedding")
    ]


def openai_chat_models() -> list[str]:
    client = OriginalOpenAI()
    response = client.models.list()
    return [
        model.model_dump()["root"]
        for model in response.data
        if str(model.model_dump()["root"]).startswith("gpt")
    ]


def gemini_embed_models() -> list[str]:
    genai.configure(transport="rest")
    response = genai.list_models()
    return [
        model.name
        for model in response
        if "embedContent" in model.supported_generation_methods
    ]


def gemini_chat_models() -> list[str]:
    genai.configure(transport="rest")
    response = genai.list_models()
    return [
        model.name
        for model in response
        if "generateContent" in model.supported_generation_methods
    ]


def ollama_embed_models() -> list[str | None]:
    client = ollama.Client(ollama_host)
    response = client.list()
    return [
        model.model
        for model in response.models
        if (model.details and model.details.family and "bert" in model.details.family)
    ]


def ollama_chat_models() -> list[str | None]:
    client = ollama.Client(ollama_host)
    response = client.list()
    return [
        model.model
        for model in response.models
        if (
            model.details is None
            or model.details.family is None
            or "bert" not in model.details.family
        )
    ]


__model_specs = {
    "openai": {
        "embed": {
            "model_class": OpenAIEmbedding,
            "model_args": {"model": openai_embed_model},
            "models_func": openai_embed_models,
        },
        "chat": {
            "model_class": OpenAI,
            "model_args": {"model": openai_chat_model},
            "models_func": openai_chat_models,
        },
    },
    "gemini": {
        "embed": {
            "model_class": GeminiEmbedding,
            "model_args": {"model": gemini_embed_model, "transport": "rest"},
            "models_func": gemini_embed_models,
        },
        "chat": {
            "model_class": Gemini,
            "model_args": {"model": gemini_chat_model, "transport": "rest"},
            "models_func": gemini_chat_models,
        },
    },
    "ollama": {
        "embed": {
            "model_class": NormOllamaEmbedding,
            "model_args": {
                "base_url": ollama_base_url,
                "model_name": ollama_embed_model,
            },
            "models_func": ollama_embed_models,
        },
        "chat": {
            "model_class": Ollama,
            "model_args": {
                "base_url": ollama_base_url,
                "model": ollama_chat_model,
            },
            "models_func": ollama_chat_models,
        },
    },
}


def get_model_providers() -> list[str]:
    import engine.extension as ext

    ext_model_providers = ext.get_model_providers()
    return list(__model_specs.keys()) + ext_model_providers


__model_lists: dict[str, dict[str, list[str]]] = {"embed": {}, "chat": {}}


def get_models(model_type: str, reload: bool) -> list[str]:
    model_provider = config.model_provider
    model_list = __model_lists[model_type].get(model_provider)
    if model_list is None or reload:
        model_spec = __model_specs.get(model_provider)
        if model_spec:
            model_list = model_spec[model_type]["models_func"]()
            __model_lists[model_type][model_provider] = model_list
        else:
            import engine.extension as ext

            model_list = ext.get_models(model_provider, model_type)
            __model_lists[model_type][model_provider] = model_list
    return model_list


def get_embed_model_name() -> str:
    return get_model_config(config.model_provider)["embed_model"]


def get_chat_model_name() -> str:
    return get_model_config(config.model_provider)["chat_model"]


def get_model_config(model_provider: str) -> dict:
    model_spec = __model_specs.get(model_provider)
    if model_spec:
        embed_model_args: dict = model_spec["embed"]["model_args"]
        embed_model = embed_model_args.get("model") or embed_model_args.get(
            "model_name"
        )
        chat_model = model_spec["chat"]["model_args"]["model"]
        return {"embed_model": embed_model, "chat_model": chat_model}
    else:
        import engine.extension as ext

        return ext.get_model_config(model_provider)


def update_model_config(model_provider: str, conf: dict):
    model_spec = __model_specs.get(model_provider)
    if model_spec:
        embed_model_args = model_spec["embed"]["model_args"]
        if "model" in embed_model_args:
            embed_model_args["model"] = conf.get("embed_model")
        if "model_name" in embed_model_args:
            embed_model_args["model_name"] = conf.get("embed_model")
        model_spec["chat"]["model_args"]["model"] = conf.get("chat_model")
    else:
        import engine.extension as ext

        ext.update_model_config(model_provider, conf)


def new_model(model_type: str) -> BaseEmbedding | LLM:
    model_provider = config.model_provider
    model_spec = __model_specs.get(model_provider)
    if model_spec:
        model_class = model_spec[model_type]["model_class"]
        model_args = model_spec[model_type]["model_args"]
        return model_class(**model_args)
    else:
        import engine.extension as ext

        return ext.new_model(model_provider, model_type)


def get_embed_model() -> BaseEmbedding:
    return caches.get_embed_model(lambda: new_model("embed"))


def get_chat_model() -> LLM:
    return caches.get_chat_model(lambda: new_model("chat"))


if __name__ == "__main__":
    print(__model_specs)
