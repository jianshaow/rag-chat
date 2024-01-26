import os
from llama_index.embeddings import OpenAIEmbedding

data_base_dir = os.environ.get("DATA_BASE_DIR", "data")
chroma_db_dir = os.environ.get("CHROMA_DB_DIR", "chroma_db")


def embedding_model():
    return OpenAIEmbedding()

def get_question():
    return "What did the author do growing up?"
