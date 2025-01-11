import logging
from llama_index.core import StorageContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.callbacks import CallbackManager

from app.engine import models, vector_db, data_store, events, caches

logger = logging.getLogger(__name__)


def create_or_load_index(
    embed_model: BaseEmbedding, data_name: str, data_dir: str
) -> VectorStoreIndex:
    callback_manager = CallbackManager([events.event_handler])
    vector_store = vector_db.get_vector_store(data_name)
    if vector_db.has_data(vector_store):
        logging.info("Loading index from vector store...")
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model,
            callback_manager=callback_manager,
        )
    else:
        documents = SimpleDirectoryReader(data_dir).load_data(show_progress=True)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context,
            embed_model=embed_model,
            callback_manager=callback_manager,
            show_progress=True,
        )
    return index


def get_index(data_name: str) -> VectorStoreIndex:
    embed_model_name = models.get_embed_model_name()
    index_key = f"{data_name}@{embed_model_name}"

    def new_index() -> VectorStoreIndex:
        data_dir = data_store.get_data_dir(data_name)
        if data_dir is not None:
            embed_model = models.get_embed_model()
            index = create_or_load_index(embed_model, data_name, data_dir)
        else:
            raise ValueError(f"Data {data_name} not found.")
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
