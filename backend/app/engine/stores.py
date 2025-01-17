from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.core.storage.docstore import SimpleDocumentStore

from app.engine import vector_db

def get_docstore(storage_dir: str) -> SimpleDocumentStore:
    return SimpleDocumentStore.from_persist_dir(storage_dir)

def get_vector_store(data_dir: str) -> ChromaVectorStore:
    chroma_collection = vector_db.get_collection(data_dir)
    ChromaVectorStore.from_collection(chroma_collection)
    return ChromaVectorStore.from_collection(chroma_collection)


def has_data(vector_store: ChromaVectorStore):
    ids = vector_store.query(VectorStoreQuery()).ids
    length = len(ids) if ids else 0
    return length != 0
