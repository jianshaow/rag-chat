from typing import List
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.schema import Document
from llama_index.core import StorageContext, VectorStoreIndex

from llama_index.core.callbacks import CallbackManager

from app.engine import models, stores, loaders, data_store, events, caches, config


def index_docs(
    documents: List[Document], vector_store: ChromaVectorStore
) -> VectorStoreIndex:
    embed_model = models.get_embed_model()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    callback_manager = CallbackManager([events.event_handler])
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context,
        embed_model=embed_model,
        callback_manager=callback_manager,
        show_progress=True,
    )

    storage_context.persist(config.get_storage_path())
    return index


def load_index(vector_store: ChromaVectorStore) -> VectorStoreIndex:
    embed_model = models.get_embed_model()
    callback_manager = CallbackManager([events.event_handler])
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model,
        callback_manager=callback_manager,
    )

    return index


def get_index(data_dir: str) -> VectorStoreIndex:
    embed_model_name = models.get_embed_model_name()
    index_key = f"{data_dir}@{embed_model_name}"

    vector_store = stores.get_vector_store(data_dir)

    if stores.has_data(vector_store):
        new_index = lambda: load_index(vector_store)
    else:
        documents = loaders.load_documents(data_dir)
        new_index = lambda: index_docs(documents, vector_store)

    return caches.get_index(new_index, index_key)


if __name__ == "__main__":
    import sys

    data_name = len(sys.argv) >= 2 and sys.argv[1] or data_store.get_data_dirs()[0]
    question = (
        len(sys.argv) >= 3 and sys.argv[2] or data_store.get_default_question(data_name)
    )
    retriever = get_index(data_name).as_retriever()
    nodes = retriever.retrieve(question)
    for node in nodes:
        print("-" * 80)
        print(node)
