import os

from pydantic import BaseModel

from app.engine import (
    CHROMA_BASE_DIR,
    DATA_BASE_DIR,
    DATA_DIR,
    MODEL_PROVIDER,
    STORAGE_BASE_DIR,
    UPLOADED_DATA_DIR,
)


class Config(BaseModel):
    data_dir: str = DATA_DIR
    model_provider: str = MODEL_PROVIDER


__config = Config()


def get_config() -> dict:
    return __config.model_dump()


def update_config(conf: dict):
    __config.__dict__.update(conf)


def get_model_provider():
    return __config.model_provider


def get_data_base_dir():
    return DATA_BASE_DIR


def get_data_dir():
    return __config.data_dir


def get_db_path():
    return os.path.join(CHROMA_BASE_DIR, __config.model_provider)


def get_data_path(data: str = __config.data_dir):
    return os.path.join(DATA_BASE_DIR, data)


def get_uploaded_data_path():
    return os.path.join(DATA_BASE_DIR, UPLOADED_DATA_DIR)


def get_data_file_path(data_dir: str, filename: str):
    return os.path.join(get_data_path(data_dir), filename)


def get_uploaded_data_file_path(filename: str):
    return os.path.join(get_uploaded_data_path(), filename)


def get_storage_path(data_dir: str) -> str:
    return os.path.join(STORAGE_BASE_DIR, __config.model_provider, data_dir)


if __name__ == "__main__":
    print(get_config())
