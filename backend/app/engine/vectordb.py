from chromadb import Collection, PersistentClient
from chromadb.api import ClientAPI
from chromadb.api.types import Document, Embedding, Metadata

from app.engine import models, setting

__db_clients: dict[str, ClientAPI] = {}


def get_db_client() -> ClientAPI:
    client = __db_clients.get(setting.get_model_provider())
    if client is None:
        path = setting.get_db_path()
        client = PersistentClient(path)
        __db_clients[setting.get_model_provider()] = client
    return client


def get_collection(data_dir: str) -> Collection:
    client = get_db_client()
    collection_name = _get_collection_name(data_dir)
    return client.get_or_create_collection(collection_name)


def _get_collection_name(data_dir: str) -> str:
    return data_dir + "__" + models.get_escaped_embed_model_name()


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
    print("=" * 80)
    client = get_db_client()
    collections = client.list_collections()
    print("database:", client.get_settings().persist_directory)
    print("collections size:", len(collections))
    print("=" * 80)
    for collection in collections:
        __show_collection(collection, 2)


def __show_collection(collection: Collection, top_k: int = 2):
    print("collection name:", collection.name)
    count = collection.count()
    print("record count:", count)
    result = collection.peek(top_k)
    ids = result["ids"]
    metadatas = result["metadatas"] if result["metadatas"] else []
    embeddings = result["embeddings"] if result["embeddings"] is not None else []
    documents = result["documents"] if result["documents"] else []
    print("top", len(metadatas), "results")
    for i, metadatas in enumerate(metadatas):
        print("-" * 70)
        print("id:", ids[i])
        __show_metadata(metadatas)
        __show_embeddings(embeddings[i])  # type: ignore
        __show_document(documents[i])
    print("-" * 80)


def __show_metadata(metadata: Metadata):
    import json

    node_content_json = metadata["_node_content"]
    node_content = json.loads(str(node_content_json) if node_content_json else "")
    node_metadata: dict = node_content["metadata"]
    print("-" * 30, "metadata", "-" * 30)
    print("file_name:", node_metadata.get("file_name"))
    print("page_label:", node_metadata.get("page_label"))
    print("data_dir:", node_metadata.get("data_dir"))
    print("private:", node_metadata.get("private"))
    print(
        "char_index:",
        node_content.get("start_char_idx"),
        "->",
        node_content.get("end_char_idx"),
    )
    print("-" * 70)


def __show_document(document: Document, unwrap=False):
    import textwrap

    if unwrap:
        print("full text:\n", document)
    else:
        print(f"{textwrap.fill("text: " + document[:347] + "...")}")


def __show_embeddings(embedding: Embedding):
    print("embedding dimension:", len(embedding))
    print("embedding:", embedding[:5])


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
                doc_id = len(sys.argv) > 3 and sys.argv[3] or None
                if doc_id is None:
                    print("provide the doc_id")
                else:
                    vector_text = get_doc_text(data_dir, [doc_id])
                    text = vector_text[0] if vector_text else ""
                    unwrap = len(sys.argv) > 4 and sys.argv[4] == "unwrap" or False
                    __show_document(text, unwrap)
        else:
            print("'cls, rm, get, doc' the cmd are supported")
    else:
        __show_db()


if __name__ == "__main__":
    _main()
