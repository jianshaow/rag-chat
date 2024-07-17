import os

from openai import OpenAI as OriginalOpenAI
import google.generativeai as genai
import ollama

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini
from llama_index.llms.ollama import Ollama

from engine import config


ollama_host = os.environ.get("OLLAMA_HOST", "localhost")
ollama_base_url = os.environ.get("OLLAMA_BASE_URL", f"http://${ollama_host}:11434")


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
    return [obj["name"] for obj in models["models"]]


__model_spec = {
    "openai": {
        "embed": {
            "model_class": OpenAIEmbedding,
            "model_args": {},
        },
        "chat": {
            "model_class": OpenAI,
            "model_args": {"model": "gpt-3.5-turbo"},
        },
        "models_func": openai_models,
    },
    "gemini": {
        "embed": {
            "model_class": GeminiEmbedding,
            "model_args": {"transport": "rest"},
        },
        "chat": {
            "model_class": Gemini,
            "model_args": {"model": "models/gemini-1.5-flash", "transport": "rest"},
        },
        "models_func": google_models,
    },
    "ollama": {
        "embed": {
            "model_class": OllamaEmbedding,
            "model_args": {
                "base_url": ollama_base_url,
                "model_name": os.environ.get(
                    "OLLAMA_EMBED_MODEL", "nomic-embed-text:v1.5"
                ),
            },
        },
        "chat": {
            "model_class": Ollama,
            "model_args": {
                "base_url": ollama_base_url,
                "model": os.environ.get("OLLAMA_CHAT_MODEL", "vicuna:7b"),
            },
        },
        "models_func": ollama_models,
    },
}


def get_api_specs():
    import engine.extension as ext

    ext_api_specs = ext.get_api_specs()
    return list(__model_spec.keys()) + ext_api_specs


__models = {}


def get_models(reload=False):
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


def new_model(api_spec, model_type):
    model_spec = __model_spec.get(api_spec)
    if model_spec:
        model_class = model_spec[model_type]["model_class"]
        model_args = model_spec[model_type]["model_args"]
        return model_class(**model_args)
    else:
        import engine.extension as ext

        return ext.new_model(api_spec, model_type)


if __name__ == "__main__":
    print(__model_spec)
