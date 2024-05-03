import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.vector_stores import VectorStoreQuery

from engine import config

__dbs: dict = {}


def get_db():
    global __dbs
    model_spec = config.model_spec
    db = __dbs.get(model_spec)
    if db is None:
        path=config.get_db_path()
        db = chromadb.PersistentClient(path)
        __dbs[model_spec] = db
    return db


def get_collection(collection_name):
    db = get_db()
    return db.get_or_create_collection(collection_name)


def get_vector_store(data_name):
    collection_name = __get_collection_name(data_name)
    chroma_collection = get_collection(collection_name)
    return ChromaVectorStore(chroma_collection=chroma_collection)


def has_data(vector_store):
    ids = vector_store.query(VectorStoreQuery()).ids
    return len(ids) != 0


def __delete_collection(collection_name):
    db = get_db()
    db.delete_collection(collection_name)


def __get_collection_name(data_name):
    return "c_" + data_name


def __show_db():
    collections = get_db().list_collections()
    print("collections size:", len(collections))
    print("===================")
    for collection in collections:
        print(collection)
        count = collection.count()
        print("record count:", count)
        vectors = collection.peek(1)
        for embeddings in vectors["embeddings"]:
            print("embeddings dimension:", len(embeddings))
            print(embeddings[:4])
        print("-------------------")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2:
        if sys.argv[1] == "rm":
            collection = len(sys.argv) == 3 and sys.argv[2] or None
            if collection is None:
                print("provide the collection name")
            else:
                __delete_collection(collection)
        else:
            print("rm is only one supported cmd")
    else:
        __show_db()
