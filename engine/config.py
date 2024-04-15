import os
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini

data_root_dir = os.environ.get("DATA_ROOT_DIR", "data")
chroma_db_dir = os.environ.get("CHROMA_DB_DIR", "chroma")
model_config_name = os.environ.get("RAG_MODEL_CONFIG", "openai")

default_data_name = "__root"
default_question = "What did the author do growing up?"


__model_config = {
    "openai": {
        "en_embed_model": os.environ.get(
            "EN_EMBED_MODEL", OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002
        ),
        "zh_embed_model": os.environ.get(
            "ZH_EMBED_MODEL", OpenAIEmbeddingModelType.TEXT_EMBED_3_LARGE
        ),
        "default_embed_model": OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002,
        "embed_model_class": OpenAIEmbedding,
        "llm_model_class": OpenAI,
    },
    "gemini": {
        "en_embed_model": "znbang/bge:large-en-v1.5-f16",
        "zh_embed_model": "znbang/bge:large-en-v1.5-f16",
        "default_embed_model": "znbang/bge:large-en-v1.5-f16",
        "embed_model_class": GeminiEmbedding,
        "llm_model_class": Gemini,
    },
}


def get_db_path():
    return os.path.join(chroma_db_dir, model_config_name)


def get_model_config():
    return __model_config[model_config_name]


def embed_model(data_name=default_data_name):
    model_config = get_model_config()
    if data_name.startswith("en"):
        model = model_config["en_embed_model"]
    elif data_name.startswith("zh"):
        model = model_config["zh_embed_model"]
    else:
        model = model_config["default_embed_model"]
    model_class = model_config["embed_model_class"]
    return model_class(model=model)


def chat_model():
    model_config = get_model_config()
    model_class = model_config["llm_model_class"]
    return model_class()
