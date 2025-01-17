from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.vector_stores import VectorStoreQuery

from app.engine import vector_db


def get_vector_store(data_name: str) -> ChromaVectorStore:
    chroma_collection = vector_db.get_collection(data_name)
    ChromaVectorStore.from_collection(chroma_collection)
    return ChromaVectorStore.from_collection(chroma_collection)


def has_data(vector_store: ChromaVectorStore):
    ids = vector_store.query(VectorStoreQuery()).ids
    length = len(ids) if ids else 0
    return length != 0
