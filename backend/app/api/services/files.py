import os, logging, uuid, re, mimetypes, base64
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field

from app.api import files_base_url
from app.engine import config

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
    file_data, extension = _preprocess_base64_file(content)
    document_file = save_file(file_data, name)
    return document_file


def save_file(
    content: bytes | str,
    file_name: str,
    save_dir: Optional[str] = None,
) -> DocumentFile:
    if save_dir is None:
        save_dir = "uploaded"

    file_id = str(uuid.uuid4())
    name, extension = os.path.splitext(file_name)
    extension = extension.lstrip(".")
    sanitized_name = _sanitize_file_name(name)
    if extension == "":
        raise ValueError("File is not supported!")
    new_file_name = f"{sanitized_name}_{file_id}.{extension}"

    file_path = os.path.join(
        os.path.join(config.get_data_base_path(), save_dir), new_file_name
    )

    if isinstance(content, str):
        content = content.encode()

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            file.write(content)
    except PermissionError as e:
        logger.error(f"Permission denied when writing to file {file_path}: {str(e)}")
        raise
    except IOError as e:
        logger.error(f"IO error occurred when writing to file {file_path}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error when writing to file {file_path}: {str(e)}")
        raise

    logger.info(f"Saved file to {file_path}")

    file_size = os.path.getsize(file_path)

    file_url = os.path.join(
        files_base_url,
        save_dir,
        new_file_name,
    )

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
