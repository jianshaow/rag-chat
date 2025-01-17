from pathlib import Path
from typing import List

from llama_index.core.schema import Document
from llama_index.core import SimpleDirectoryReader
from llama_index.core.readers.file.base import default_file_metadata_func

from app.engine import data_store


def load_doc_from_dir(data_dir: str) -> List[Document]:
    data_path = data_store.get_data_path(data_dir)
    reader = SimpleDirectoryReader(data_path, filename_as_id=True)
    documents = reader.load_data(show_progress=True)
    return documents


def load_doc_from_file(file_path: str) -> List[Document]:
    documents = SimpleDirectoryReader.load_file(
        Path(file_path),
        filename_as_id=True,
        file_metadata=default_file_metadata_func,
        file_extractor={},
    )
    return documents
