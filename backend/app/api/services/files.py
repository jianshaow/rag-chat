import os, logging, uuid, re, mimetypes, base64
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field

from llama_index.core import VectorStoreIndex
from llama_index.core.schema import Document

from app.api import files_base_url
from app.engine import config, indexes, loaders, utils, UPLOADED_DATA_DIR

logger = logging.getLogger(__name__)


class DocumentFile(BaseModel):
    id: str
    name: str
    type: str
    size: int
    url: str
    path: Optional[str] = Field(
        None,
        exclude=True,
    )
    refs: Optional[List[str]] = Field(None)


def process_file(
    name: str, content: str, params: Optional[dict] = None
) -> DocumentFile:
    file_data, _ = _preprocess_base64_file(content)
    document_file = save_file(file_data, name)
    documents = _load_file_to_documents(document_file)
    index = indexes.get_index(UPLOADED_DATA_DIR)
    _add_documents_to_vector_store_index(documents, index)
    document_file.refs = [doc.doc_id for doc in documents]
    return document_file


def save_file(
    content: bytes | str,
    file_name: str,
) -> DocumentFile:
    file_id = str(uuid.uuid4())
    name, extension = os.path.splitext(file_name)
    extension = extension.lstrip(".")
    sanitized_name = _sanitize_file_name(name)
    if extension == "":
        raise ValueError("File is not supported!")
    new_file_name = f"{sanitized_name}_{file_id}.{extension}"

    file_path = config.get_uploaded_data_file_path(new_file_name)

    if isinstance(content, str):
        content = content.encode()

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb", encoding="utf-8") as file:
            file.write(content)
    except PermissionError as e:
        logger.error("Permission denied when writing to file %s: %s", file_path, e)
        raise
    except IOError as e:
        logger.error("IO error occurred when writing to file %s: %s", file_path, e)
        raise
    except Exception as e:
        logger.error("Unexpected error when writing to file %s: %s", file_path, e)
        raise

    logger.info("Saved file to %s", file_path)

    file_size = os.path.getsize(file_path)

    file_url = os.path.join(files_base_url, UPLOADED_DATA_DIR, new_file_name)

    return DocumentFile(
        id=file_id,
        name=new_file_name,
        type=extension,
        size=file_size,
        path=file_path,
        url=file_url,
        refs=None,
    )


def _sanitize_file_name(file_name: str) -> str:
    sanitized_name = re.sub(r"[^a-zA-Z0-9.]", "_", file_name)
    return sanitized_name


def _preprocess_base64_file(base64_content: str) -> Tuple[bytes, str | None]:
    header, data = base64_content.split(",", 1)
    mime_type = header.split(";")[0].split(":", 1)[1]
    guessed_extension = mimetypes.guess_extension(mime_type)
    extension = guessed_extension.lstrip(".") if guessed_extension else ""
    return base64.b64decode(data), extension


def _load_file_to_documents(file: DocumentFile) -> List[Document]:
    assert file.path, "File path is not set!"
    documents = loaders.load_doc_from_file(file.path)
    for doc in documents:
        doc.metadata["private"] = "true"
        doc.metadata["data_dir"] = UPLOADED_DATA_DIR
    return documents


def _add_documents_to_vector_store_index(
    documents: List[Document], index: VectorStoreIndex
) -> None:
    utils.log_model_info(UPLOADED_DATA_DIR)

    nodes = indexes.ingest(documents, UPLOADED_DATA_DIR)

    if index is None:
        index = VectorStoreIndex(nodes=nodes, show_progress=True)
    else:
        index.insert_nodes(nodes=nodes, show_progress=True)
