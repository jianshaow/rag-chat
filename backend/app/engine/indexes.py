import logging, os
from llama_index.core import StorageContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.callbacks import CallbackManager

from app.engine import models, vector_db, data_store, events, caches

logger = logging.getLogger(__name__)


def index_data(embed_model: BaseEmbedding, data_dir: str) -> VectorStoreIndex:
    vector_store = vector_db.get_vector_store(data_dir)
    data_path = data_store.get_data_path(data_dir)

    def add_metadata(file_name: str) -> dict:
        file_name = os.path.basename(file_name)
        return {
            "file_name": file_name,
            "private": "false",
            "data_dir": data_dir,
        }

    documents = SimpleDirectoryReader(data_path, file_metadata=add_metadata).load_data(
        show_progress=True
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    callback_manager = CallbackManager([events.event_handler])
    logging.info("index data dir '%s' into vector store...", data_dir)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context,
        embed_model=embed_model,
        callback_manager=callback_manager,
        show_progress=True,
    )

    return index


def load_index(embed_model: BaseEmbedding, data_name: str) -> VectorStoreIndex:
    callback_manager = CallbackManager([events.event_handler])
    vector_store = vector_db.get_vector_store(data_name)
    logging.info("Loading index '%s' from vector store...", data_name)
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model,
        callback_manager=callback_manager,
    )

    return index


def get_index(data_name: str) -> VectorStoreIndex:
    embed_model_name = models.get_embed_model_name()
    index_key = f"{data_name}@{embed_model_name}"

    def new_index() -> VectorStoreIndex:
        embed_model = models.get_embed_model()
        index = load_index(embed_model, data_name)
        return index

    return caches.get_index(new_index, index_key)


if __name__ == "__main__":
    import sys

    data_name = len(sys.argv) >= 2 and sys.argv[1] or data_store.get_data_names()[0]
    question = (
        len(sys.argv) >= 3 and sys.argv[2] or data_store.get_default_question(data_name)
    )
    retriever = get_index(data_name).as_retriever()
    nodes = retriever.retrieve(question)
    for node in nodes:
        print("-" * 80)
        print(node)
