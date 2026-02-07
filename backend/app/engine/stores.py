import os

from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.core.storage.docstore.types import DEFAULT_PERSIST_FNAME
from llama_index.core.storage.docstore import SimpleDocumentStore

from app.engine import vectordb


def get_docstore(storage_dir: str) -> SimpleDocumentStore:
    if os.path.exists(os.path.join(storage_dir, DEFAULT_PERSIST_FNAME)):
        return SimpleDocumentStore.from_persist_dir(storage_dir)
    else:
        return SimpleDocumentStore()


def get_vector_store(data_dir: str) -> ChromaVectorStore:
    chroma_collection = vectordb.get_collection(data_dir)
    return ChromaVectorStore.from_collection(chroma_collection)


def has_data(vector_store: ChromaVectorStore):
    ids = vector_store.query(VectorStoreQuery()).ids
    length = len(ids) if ids else 0
    return length != 0
