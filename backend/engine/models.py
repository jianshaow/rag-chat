import os
from engine import config
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini
from llama_index.llms.ollama import Ollama

__model_spec = {
    "openai": {
        "embed": {
            "model_class": OpenAIEmbedding,
            "model_args": {},
        },
        "chat": {
            "model_class": OpenAI,
            "model_args": {},
        },
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
    },
    "ollama": {
        "embed": {
            "model_class": OllamaEmbedding,
            "model_args": {
                "base_url": os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
                "model_name": os.environ.get(
                    "OLLAMA_EMBED_MODEL", "nomic-embed-text:v1.5"
                ),
            },
        },
        "chat": {
            "model_class": Ollama,
            "model_args": {
                "base_url": os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
                "model": os.environ.get("OLLAMA_CHAT_MODEL", "vicuna:7b"),
            },
        },
    },
}


def get_api_specs():
    return list(__model_spec.keys())


def get_model_spec():
    return __model_spec[config.api_spec]


def new_model(model_type):
    model_spec = get_model_spec()
    model_class = model_spec[model_type]["model_class"]
    model_args = model_spec[model_type]["model_args"]
    return model_class(**model_args)


if __name__ == "__main__":
    print(__model_spec)
