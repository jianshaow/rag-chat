from llama_index.core import StorageContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.base.embeddings.base import BaseEmbedding

from engine import config, models, vector_db, data_store

__indexes: dict[str, VectorStoreIndex] = {}


def create_or_load_index(
    embed_model: BaseEmbedding, data_name, data_dir
) -> VectorStoreIndex:
    vector_store = vector_db.get_vector_store(data_name)
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


def get_index(data_name) -> VectorStoreIndex:
    embed_model_name = models.get_embed_model_name()
    index_key = f"{data_name}@{embed_model_name}@{config.model_provider}"
    index = __indexes.get(index_key)
    if index is None:
        data_dir = data_store.get_data_dir(data_name)
        if data_dir is not None:
            embed_model = models.new_model(config.model_provider, "embed")
            index = create_or_load_index(embed_model, data_name, data_dir)
            __indexes[index_key] = index
    return index


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
