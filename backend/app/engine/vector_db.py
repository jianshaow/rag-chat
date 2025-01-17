import chromadb
from chromadb import Collection
from chromadb.api import ClientAPI
from chromadb.api.types import Document, Metadata, Embedding

from app.engine import config, models

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
    collection_name = _get_collection_name(data_name)
    return client.get_or_create_collection(collection_name)


def _get_collection_name(data_name: str) -> str:
    escaped = models.get_embed_model_name().replace(":", "_").replace("/", "_")
    return data_name + "__" + escaped


def get_doc_text(data_name, ids: list[str]):
    collection = get_collection(data_name)
    result = collection.get(ids)
    return result["documents"]


def __clear_data_vector(data_name: str):
    collection = get_collection(data_name)
    ids = collection.peek()["ids"]
    while len(ids) > 0:
        collection.delete(ids)
        ids = collection.peek()["ids"]


def __delete_data_collection(data_name):
    client = get_db_client()
    client.delete_collection(_get_collection_name(data_name))


def __show_db():
    collections = get_db_client().list_collections()
    print("collections size:", len(collections))
    print("=" * 80)
    for collection in collections:
        __show_collection(collection)


def __show_collection(collection: Collection):
    print("collection name:", collection.name)
    count = collection.count()
    print("record count:", count)
    result = collection.peek(1)
    metadatas = result["metadatas"] if result["metadatas"] else []
    embeddings = result["embeddings"] if result["embeddings"] is not None else []
    documents = result["documents"] if result["documents"] else []
    print("top", len(metadatas), "results")
    for i, metadatas in enumerate(metadatas):
        __show_metadata(metadatas)
        __show_embeddings(embeddings[i])  # type: ignore
        __show_document(documents[i])
    print("-" * 80)


def __show_metadata(metadata: Metadata):
    import json

    print("+" * 80)
    node_content_json = metadata["_node_content"]
    node_content = json.loads(str(node_content_json) if node_content_json else "")
    node_metadata = node_content["metadata"]
    print("file name:", node_metadata["file_name"])
    print("data dir:", node_metadata["data_dir"])
    print(
        "char index:",
        node_content["start_char_idx"],
        "->",
        node_content["end_char_idx"],
    )


def __show_document(document: Document):
    import textwrap

    print("+" * 80)
    print(f"document:\n{textwrap.fill(document[:347])}...")


def __show_embeddings(embedding: Embedding):
    print("+" * 80)
    print("embedding dimension:", len(embedding))
    print(embedding[:4])


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "cls":
            data_name = len(sys.argv) == 3 and sys.argv[2] or None
            if data_name:
                __clear_data_vector(data_name)
            else:
                print("provide the data name")
        elif sys.argv[1] == "rm":
            data_name = len(sys.argv) == 3 and sys.argv[2] or None
            if data_name is None:
                print("provide the collection name")
            else:
                __delete_data_collection(data_name)
        elif sys.argv[1] == "get":
            data_name = len(sys.argv) >= 3 and sys.argv[2] or None
            if data_name is None:
                print("provide the data_name")
            else:
                id = len(sys.argv) >= 4 and sys.argv[3] or None
                if id is None:
                    collection = get_collection(data_name)
                    __show_collection(collection)
                else:
                    vector_text = get_doc_text(data_name, [id])
                    text = vector_text[0] if vector_text else ""
                    __show_document(text)
        else:
            print("cls, rm, get are supported cmd")
    else:
        __show_db()
