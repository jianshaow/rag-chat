from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    SimpleDirectoryReader,
)

from engine import config, vector_db, data_store

__indexes = {}


def create_or_load_index(data_name, data_dir):
    vector_store = vector_db.get_vector_store(data_name)
    embed_model = config.embed_model(data_name)
    print("model_spec:", config.model_spec)
    print("data_name:", data_name)
    print("embed_model:", embed_model.model_name)
    if vector_db.has_data(vector_store):
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model,
        )
    else:
        documents = SimpleDirectoryReader(data_dir).load_data(show_progress=True)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context,
            embed_model=embed_model,
            show_progress=True,
        )
    return index


def get_index(data_name):
    global __indexes
    index_key = "{data_name}@{model_spec}".format(
        data_name=data_name, model_spec=config.model_spec
    )
    index = __indexes.get(index_key)
    if index is None:
        data_dir = data_store.get_data_dir(data_name)
        if data_dir is not None:
            index = create_or_load_index(data_name, data_dir)
            __indexes[index_key] = index
    return index


if __name__ == "__main__":
    import sys

    data_name = len(sys.argv) >= 2 and sys.argv[1] or data_store.get_data_names()[0]
    question = (
        len(sys.argv) >= 3 and sys.argv[2] or data_store.get_default_question(data_name)
    )
    retriever = get_index(data_name=data_name).as_retriever()
    nodes = retriever.retrieve(question)
    for node in nodes:
        print("---------------------------------------------")
        print(node)
