import chromadb
from llama_index import ServiceContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext

from engine import config, data_store

__indexes = {}


def initialize_index(data_name, data_path):
    global __indexes
    db = chromadb.PersistentClient(path=config.chroma_db_dir)
    collection_name = __get_collection_name(data_name)
    chroma_collection = db.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    service_context = ServiceContext.from_defaults(
        embed_model=config.embedding_model(), llm=config.chat_model()
    )
    print("embed_model:", service_context.embed_model.model_name)
    print("chat_model:", service_context.llm.model)
    if chroma_collection.count() == 0:
        documents = SimpleDirectoryReader(data_path).load_data(show_progress=True)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            service_context=service_context,
            show_progress=True,
        )
    else:
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            service_context=service_context,
        )
    __indexes[data_name] = index
    return index


def get_index(data_name=config.default_data_name):
    global __indexes
    index = __indexes.get(data_name)
    if index is None:
        data_path = data_store.get_data_path(data_name)
        if data_path is not None:
            index = initialize_index(data_name, data_path)
    return index


def __get_collection_name(data_name):
    return "c_" + data_name


if __name__ == "__main__":
    retriever = get_index().as_retriever()
    question = config.get_question()
    nodes = retriever.retrieve(question)
    for node in nodes:
        print(node)
