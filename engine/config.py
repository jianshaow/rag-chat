import os
from llama_index.embeddings import OpenAIEmbedding
from llama_index.llms import OpenAI

data_root_dir = os.environ.get("DATA_ROOT_DIR", "data")
chroma_db_dir = os.environ.get("CHROMA_DB_DIR", "chroma_db")
default_data_name = "__root"


def embedding_model():
    return OpenAIEmbedding()


def chat_model():
    return OpenAI()


def get_question():
    return "What did the author do growing up?"
