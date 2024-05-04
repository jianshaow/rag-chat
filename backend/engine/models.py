import os
from engine import config
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini

__model_spec = {
    "openai": {
        "en_embed_model": os.environ.get(
            "EN_EMBED_MODEL", OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002
        ),
        "zh_embed_model": os.environ.get(
            "ZH_EMBED_MODEL", OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002
        ),
        "default_embed_model": OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002,
        "embed_model_class": OpenAIEmbedding,
        "llm_model_class": OpenAI,
    },
    "gemini": {
        "embed_model_class": GeminiEmbedding,
        "llm_model_class": Gemini,
    },
}


def get_model_spec():
    return __model_spec[config.model_spec]


def embed_model(data_name: str):
    model_spec = get_model_spec()
    model_class = model_spec["embed_model_class"]

    if model_class == OpenAIEmbedding:
        if data_name.startswith("en"):
            model = model_spec["en_embed_model"]
        elif data_name.startswith("zh"):
            model = model_spec["zh_embed_model"]
        else:
            model = model_spec["default_embed_model"]
        return model_class(model=model)

    return model_class()


def chat_model():
    model_spec = get_model_spec()
    model_class = model_spec["llm_model_class"]
    return model_class()


if __name__ == "__main__":
    print(__model_spec)
