from chromadb import Collection, PersistentClient
from chromadb.api import ClientAPI
from chromadb.api.types import Document, Embedding, Metadata

from app.engine import config, models

__db_clients: dict[str, ClientAPI] = {}


def get_db_client() -> ClientAPI:
    client = __db_clients.get(config.get_model_provider())
    if client is None:
        path = config.get_db_path()
        client = PersistentClient(path)
        __db_clients[config.get_model_provider()] = client
    return client


def get_collection(data_dir: str) -> Collection:
    client = get_db_client()
    collection_name = _get_collection_name(data_dir)
    return client.get_or_create_collection(collection_name)


def _get_collection_name(data_dir: str) -> str:
    escaped = models.get_embed_model_name().replace(":", "_").replace("/", "_")
    return data_dir + "__" + escaped


def get_doc_text(data_dir, ids: list[str]):
    collection = get_collection(data_dir)
    result = collection.get(ids)
    return result["documents"]


def __clear_data_vector(data_dir: str):
    collection = get_collection(data_dir)
    ids = collection.peek()["ids"]
    while len(ids) > 0:
        collection.delete(ids)
        ids = collection.peek()["ids"]


def __delete_data_collection(data_dir):
    client = get_db_client()
    client.delete_collection(_get_collection_name(data_dir))


def __show_db():
    collections = get_db_client().list_collections()
    print("=" * 80)
    print("collections size:", len(collections))
    for collection in collections:
        __show_collection(collection, 1)


def __show_collection(collection: Collection, top_k: int = 2):
    print("+" * 80)
    print("collection name:", collection.name)
    count = collection.count()
    print("record count:", count)
    result = collection.peek(top_k)
    metadatas = result["metadatas"] if result["metadatas"] else []
    embeddings = result["embeddings"] if result["embeddings"] is not None else []
    documents = result["documents"] if result["documents"] else []
    print("top", len(metadatas), "results")
    for i, metadatas in enumerate(metadatas):
        __show_metadata(metadatas)
        __show_embeddings(embeddings[i])  # type: ignore
        __show_document(documents[i])
    print("+" * 80)


def __show_metadata(metadata: Metadata):
    import json

    print("-" * 80)
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

    print("-" * 80)
    print(f"document:\n{textwrap.fill(document[:347])}...")


def __show_embeddings(embedding: Embedding):
    print("-" * 80)
    print("embedding dimension:", len(embedding))
    print(embedding[:4])


def _main():
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "cls":
            data_dir = len(sys.argv) > 2 and sys.argv[2] or None
            if data_dir:
                __clear_data_vector(data_dir)
            else:
                print("provide the data name")
        elif cmd == "rm":
            data_dir = len(sys.argv) > 2 and sys.argv[2] or None
            if data_dir is None:
                print("provide the collection name")
            else:
                __delete_data_collection(data_dir)
        elif cmd == "get":
            data_dir = len(sys.argv) > 2 and sys.argv[2] or None
            if data_dir is None:
                print("provide the data_name")
            else:
                collection = get_collection(data_dir)
                top_k = len(sys.argv) > 3 and int(sys.argv[3]) or 2
                __show_collection(collection, top_k)
        elif cmd == "doc":
            data_dir = len(sys.argv) > 2 and sys.argv[2] or None
            if data_dir is None:
                print("provide the data_name")
            else:
                doc_id = len(sys.argv) > 4 and sys.argv[4] or None
                if doc_id is None:
                    print("provide the doc_id")
                else:
                    vector_text = get_doc_text(data_dir, [doc_id])
                    text = vector_text[0] if vector_text else ""
                    __show_document(text)
        else:
            print("cls, rm, get are supported cmd")
    else:
        __show_db()


if __name__ == "__main__":
    _main()
