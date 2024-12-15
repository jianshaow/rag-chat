from openai import OpenAI as OriginalOpenAI
import google.generativeai as genai
import ollama

from llama_index.core.llms import LLM
from llama_index.core.base.llms.types import ChatMessage
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini
from llama_index.llms.ollama import Ollama

from engine import (
    config,
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


def openai_models() -> list[str]:
    client = OriginalOpenAI()
    return [obj.id for obj in client.models.list().data]


def google_models() -> list[str]:
    genai.configure(transport="rest")
    return [
        model.name
        for model in genai.list_models()
        if "generateContent" in model.supported_generation_methods
    ]


def ollama_models() -> list[str]:
    client = ollama.Client(ollama_host)
    models = client.list()
    return [obj["model"] for obj in models["models"]]


__model_spec = {
    "openai": {
        "embed": {
            "model_class": OpenAIEmbedding,
            "model_args": {"model": openai_embed_model},
        },
        "chat": {
            "model_class": OpenAI,
            "model_args": {"model": openai_chat_model},
        },
        "models_func": openai_models,
    },
    "gemini": {
        "embed": {
            "model_class": GeminiEmbedding,
            "model_args": {"model": gemini_embed_model, "transport": "rest"},
        },
        "chat": {
            "model_class": Gemini,
            "model_args": {"model": gemini_chat_model, "transport": "rest"},
        },
        "models_func": google_models,
    },
    "ollama": {
        "embed": {
            "model_class": NormOllamaEmbedding,
            "model_args": {
                "base_url": ollama_base_url,
                "model_name": ollama_embed_model,
            },
        },
        "chat": {
            "model_class": Ollama,
            "model_args": {
                "base_url": ollama_base_url,
                "model": ollama_chat_model,
            },
        },
        "models_func": ollama_models,
    },
}


def get_api_specs() -> list[str]:
    import engine.extension as ext

    ext_api_specs = ext.get_api_specs()
    return list(__model_spec.keys()) + ext_api_specs


__models = {}


def get_models(reload=False) -> list[str]:
    api_spec = config.api_spec
    models = __models.get(api_spec)
    if models is None or reload:
        model_spec = __model_spec.get(api_spec)
        if model_spec:
            models = model_spec["models_func"]()
            __models[api_spec] = models
        else:
            import engine.extension as ext

            models = ext.get_models(api_spec)
            __models[api_spec] = models
    return models


def get_api_config(api_spec: str) -> dict:
    model_spec = __model_spec.get(api_spec)
    if model_spec:
        model = model_spec["chat"]["model_args"]["model"]
        return {"model": model}
    else:
        import engine.extension as ext

        return ext.get_api_config(api_spec)


def update_api_config(api_spec: str, conf: dict):
    model_spec = __model_spec.get(api_spec)
    if model_spec:
        model_spec["chat"]["model_args"]["model"] = conf.get("model")
    else:
        import engine.extension as ext

        ext.update_api_config(api_spec, conf)


def new_model(api_spec, model_type) -> LLM:
    model_spec = __model_spec.get(api_spec)
    if model_spec:
        model_class = model_spec[model_type]["model_class"]
        model_args = model_spec[model_type]["model_args"]
        return model_class(**model_args)
    else:
        import engine.extension as ext

        return ext.new_model(api_spec, model_type)


class ChatMessages:
    def __init__(self, messages: list):
        self.messages = messages

    @property
    def last(self):
        last_message = self.messages[-1]
        message_content = last_message["content"]
        return message_content

    @property
    def history(self):
        chat_messages = [
            ChatMessage(role=message["role"], content=message["content"])
            for message in self.messages[:-1]
        ]
        return chat_messages

    def __str__(self):
        return str(
            [
                {"role": message["role"], "content": message["content"]}
                for message in self.messages
            ]
        )


if __name__ == "__main__":
    print(__model_spec)
