import os
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.llms.openai import OpenAI

ZH_EMBED_MODEL = "bge-large-zh-v1.5"
EN_EMBED_MODEL = "bge-large-en-v1.5"

data_root_dir = os.environ.get("DATA_ROOT_DIR", "data")
chroma_db_dir = os.environ.get("CHROMA_DB_DIR", "chroma_db")
default_data_name = "__root"
default_question = "What did the author do growing up?"


def embed_model(data_name=default_data_name):
    if data_name.startswith("en"):
        model = EN_EMBED_MODEL
    elif data_name.startswith("zh"):
        model = ZH_EMBED_MODEL
    else:
        model = OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002
    return OpenAIEmbedding(model=model)


def chat_model():
    return OpenAI()
