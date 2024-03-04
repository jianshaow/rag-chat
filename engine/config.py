import os
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.llms.openai import OpenAI

data_root_dir = os.environ.get("DATA_ROOT_DIR", "data")
chroma_db_dir = os.environ.get("CHROMA_DB_DIR", "chroma_db")

en_embed_model = os.environ.get(
    "EN_EMBED_MODEL", OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002
)
zh_embed_model = os.environ.get(
    "ZH_EMBED_MODEL", OpenAIEmbeddingModelType.TEXT_EMBED_3_LARGE
)
default_embed_model = OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002

default_data_name = "__root"
default_question = "What did the author do growing up?"


def embed_model(data_name=default_data_name):
    if data_name.startswith("en"):
        model = en_embed_model
    elif data_name.startswith("zh"):
        model = zh_embed_model
    else:
        model = default_embed_model
    return OpenAIEmbedding(model=model)


def chat_model():
    return OpenAI()
