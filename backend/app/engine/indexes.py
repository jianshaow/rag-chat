from typing import List

from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.schema import Document
from llama_index.core.ingestion import IngestionPipeline, DocstoreStrategy
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.callbacks import CallbackManager

from app.engine import models, stores, loaders, data_store, events, caches, config


def ingest(documents: List[Document], data_dir: str):
    vector_store = stores.get_vector_store(data_dir)
    docstore = stores.get_docstore(config.get_storage_path())
    pipeline = IngestionPipeline(
        transformations=[SentenceSplitter(), models.get_embed_model()],
        docstore=docstore,
        vector_store=vector_store,
        docstore_strategy=DocstoreStrategy.UPSERTS_AND_DELETE,
    )
    nodes = pipeline.run(documents=documents, show_progress=True)
    StorageContext.from_defaults(docstore=docstore, vector_store=vector_store).persist(
        config.get_storage_path()
    )
    return nodes


def index_data(data_dir: str):
    documents = loaders.load_doc_from_dir(data_dir)
    for doc in documents:
        doc.metadata["private"] = "falses"
        doc.metadata["data_dir"] = data_dir
    return ingest(documents, data_dir)


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
    new_index = lambda: load_index(vector_store)
    return caches.get_index(new_index, index_key)


def __retrieve_data(data_dir: str):
    question = data_store.get_default_question(data_dir)
    retriever = get_index(data_dir).as_retriever()
    nodes = retriever.retrieve(question)
    for node in nodes:
        print("-" * 80)
        print(node)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "index":
            data_dir = len(sys.argv) == 3 and sys.argv[2] or None
            if data_dir:
                index_data(data_dir)
            else:
                print("Data directory not provided.")
        elif sys.argv[1] == "retrieve":
            data_dir = len(sys.argv) == 3 and sys.argv[2] or None
            if data_dir:
                __retrieve_data(data_dir)
            else:
                print("Data directory not provided.")
    else:
        __retrieve_data(data_store.get_data_dirs()[0])
