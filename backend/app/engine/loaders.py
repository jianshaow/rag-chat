from typing import List
from llama_index.core.schema import Document
from llama_index.core import SimpleDirectoryReader
from llama_index.core.readers.file.base import default_file_metadata_func

from app.engine import data_store


def load_documents(data_dir: str) -> List[Document]:
    data_path = data_store.get_data_path(data_dir)

    def add_metadata(file_name: str) -> dict:
        metadata = default_file_metadata_func(file_name)
        metadata["private"] = "false"
        metadata["data_dir"] = data_dir
        return metadata

    reader = SimpleDirectoryReader(
        data_path, filename_as_id=True, file_metadata=add_metadata
    )
    return reader.load_data(show_progress=True)
