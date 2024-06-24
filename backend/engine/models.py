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
        "embed_model_class": OpenAIEmbedding,
        "llm_model_class": OpenAI,
    },
    "gemini": {
        "embed_model_class": GeminiEmbedding,
        "llm_model_class": Gemini,
    },
    "ollama": {
        "embed_model_class": OllamaEmbedding,
        "llm_model_class": Ollama,
    },
}


def get_api_specs():
    return list(__model_spec.keys())


def get_model_spec():
    return __model_spec[config.api_spec]


def embed_model():
    model_spec = get_model_spec()
    model_class = model_spec["embed_model_class"]

    if model_class == OllamaEmbedding:
        return OllamaEmbedding(
            base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
            model_name=os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text:v1.5"),
        )

    return model_class()


def chat_model():
    model_spec = get_model_spec()
    model_class = model_spec["llm_model_class"]

    if model_class == Ollama:
        return Ollama(
            base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
            model=os.environ.get("OLLAMA_CHAT_MODEL", "vicuna:13b"),
        )
    return model_class()


if __name__ == "__main__":
    print(__model_spec)
