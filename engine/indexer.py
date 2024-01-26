import chromadb
from llama_index import ServiceContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext

from engine import config

__index = None


def initialize_index():
    global __index
    db = chromadb.PersistentClient(path=config.chroma_db_dir)
    chroma_collection = db.get_or_create_collection("local")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    service_context = ServiceContext.from_defaults(embed_model=config.embedding_model())
    print("embed_model:", service_context.embed_model.model_name)
    if chroma_collection.count() == 0:
        documents = SimpleDirectoryReader(config.data_base_dir).load_data(
            show_progress=True
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        __index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            service_context=service_context,
            show_progress=True,
        )
    else:
        __index = VectorStoreIndex.from_vector_store(
            vector_store,
            service_context=service_context,
        )


def get_index():
    global __index
    if __index is None:
        initialize_index()
    return __index


if __name__ == "__main__":
    retriever = get_index().as_retriever()
    question = config.get_question()
    nodes = retriever.retrieve(question)
    for node in nodes:
        print(node)
