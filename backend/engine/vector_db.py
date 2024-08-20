import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.vector_stores import VectorStoreQuery

from engine import config

__dbs: dict = {}


def get_db():
    global __dbs
    model_spec = config.api_spec
    db = __dbs.get(model_spec)
    if db is None:
        path = config.get_db_path()
        db = chromadb.PersistentClient(path)
        __dbs[model_spec] = db
    return db


def get_collection(data_name):
    db = get_db()
    collection_name = __get_collection_name(data_name)
    return db.get_or_create_collection(collection_name)


def get_vector_store(data_name):
    chroma_collection = get_collection(data_name)
    return ChromaVectorStore(chroma_collection=chroma_collection)


def get_vector_text(data_name, ids: list[str]):
    collection = get_collection(data_name)
    result = collection.get(ids)
    return result["documents"]


def has_data(vector_store: ChromaVectorStore):
    ids = vector_store.query(VectorStoreQuery()).ids
    return len(ids) != 0


def __clear_collection(collection_name):
    db = get_db()
    collection = db.get_collection(collection_name)
    ids = collection.peek()["ids"]
    while len(ids) > 0:
        collection.delete(ids)
        ids = collection.peek()["ids"]


def __delete_collection(collection_name):
    db = get_db()
    db.delete_collection(collection_name)


def __get_collection_name(data_name):
    return "c_" + data_name


def __show_db():
    import json

    collections = get_db().list_collections()
    print("collections size:", len(collections))
    print("=" * 80)
    for collection in collections:
        print("collection name:", collection.get_model()["name"])
        count = collection.count()
        print("record count:", count)
        result = collection.peek(1)
        for i, metadata in enumerate(result["metadatas"]):
            print("+" * 80)
            print(
                "file name:",
                json.loads(metadata["_node_content"])["metadata"]["file_name"],
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
