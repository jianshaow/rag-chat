from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    SimpleDirectoryReader,
)

from engine import config, vector_db, data_store

__indexes = {}


def create_or_load_index(data_name, data_path):
    vector_store = vector_db.get_vector_store(data_name)
    embed_model = config.embed_model(data_name)
    print("data_name:", data_name)
    print("embed_model:", embed_model.model_name)
    if vector_db.has_data(vector_store):
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model,
        )
    else:
        documents = SimpleDirectoryReader(data_path).load_data(show_progress=True)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context,
            embed_model=embed_model,
            show_progress=True,
        )
    return index


def get_index(data_name=config.default_data_name):
    global __indexes
    index = __indexes.get(data_name)
    if index is None:
        data_path = data_store.get_data_path(data_name)
        if data_path is not None:
            index = create_or_load_index(data_name, data_path)
    __indexes[data_name] = index
    return index


if __name__ == "__main__":
    import sys

    data_name = len(sys.argv) >= 2 and sys.argv[1] or config.default_data_name
    question = len(sys.argv) >= 3 and sys.argv[2] or config.default_question
    retriever = get_index(data_name=data_name).as_retriever()
    nodes = retriever.retrieve(question)
    for node in nodes:
        print("---------------------------------------------")
        print(node)
