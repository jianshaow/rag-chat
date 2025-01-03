import chromadb
from chromadb import ClientAPI, Collection
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.vector_stores import VectorStoreQuery

from engine import config, models

__db_clients: dict[str, ClientAPI] = {}


def get_db_client() -> ClientAPI:
    client = __db_clients.get(config.model_provider)
    if client is None:
        path = config.get_db_path()
        client = chromadb.PersistentClient(path)
        __db_clients[config.model_provider] = client
    return client


def get_collection(data_name: str) -> Collection:
    client = get_db_client()
    escaped = models.get_embed_model_name().replace(":", "_").replace("/", "_")
    collection_name = data_name + "__" + escaped
    return client.get_or_create_collection(collection_name)


def get_vector_store(data_name: str) -> ChromaVectorStore:
    chroma_collection = get_collection(data_name)
    return ChromaVectorStore(chroma_collection=chroma_collection)


def get_vector_text(data_name, ids: list[str]):
    collection = get_collection(data_name)
    result = collection.get(ids)
    return result["documents"]


def has_data(vector_store: ChromaVectorStore):
    ids = vector_store.query(VectorStoreQuery()).ids
    return len(ids) != 0


def __clear_collection(collection_name: str):
    client = get_db_client()
    collection = client.get_collection(collection_name)
    ids = collection.peek()["ids"]
    while len(ids) > 0:
        collection.delete(ids)
        ids = collection.peek()["ids"]


def __delete_collection(collection_name):
    client = get_db_client()
    client.delete_collection(collection_name)


def __show_db():
    import json

    collections = get_db_client().list_collections()
    print("collections size:", len(collections))
    print("=" * 80)
    for collection in collections:
        print("collection name:", collection.get_model()["name"])
        count = collection.count()
        print("record count:", count)
        result = collection.peek(1)
        for i, metadatas in enumerate(result["metadatas"]):
            print("+" * 80)
            node_content = json.loads(metadatas["_node_content"])
            metadata = node_content["metadata"]
            print("file name:", metadata["file_name"])
            print(
                "char index:",
                node_content["start_char_idx"],
                "->",
                node_content["end_char_idx"],
            )
            embedding = result["embeddings"][i]
            print("embeddings dimension:", len(embedding))
            print(embedding[:4])
        print("-" * 80)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2:
        if sys.argv[1] == "cls":
            collection = len(sys.argv) == 3 and sys.argv[2] or None
            if collection is None:
                print("provide the collection name")
            else:
                __clear_collection(collection)
        elif sys.argv[1] == "rm":
            collection = len(sys.argv) == 3 and sys.argv[2] or None
            if collection is None:
                print("provide the collection name")
            else:
                __delete_collection(collection)
        elif sys.argv[1] == "get":
            data_name = len(sys.argv) >= 3 and sys.argv[2] or None
            id = len(sys.argv) >= 4 and sys.argv[3] or None
            print(get_vector_text(data_name, [id])[0])
        else:
            print("rm is only one supported cmd")
    else:
        __show_db()
