import os

from pydantic import BaseModel

from app.engine import (
    CHROMA_BASE_DIR,
    DATA_BASE_DIR,
    DATA_DIR,
    MCP_SERVER,
    MODEL_PROVIDER,
    STORAGE_BASE_DIR,
    TOOL_SET,
    UPLOADED_DATA_DIR,
)


class Setting(BaseModel):
    model_provider: str
    tool_set: str
    data_dir: str
    mcp_server: str


__setting = Setting(
    data_dir=DATA_DIR,
    model_provider=MODEL_PROVIDER,
    tool_set=TOOL_SET,
    mcp_server=MCP_SERVER,
)


def get_config() -> Setting:
    return __setting


def update_config(new_setting: Setting):
    __setting.__dict__.update(new_setting.model_dump())


def get_model_provider():
    return __setting.model_provider


def get_tool_set():
    return __setting.tool_set


def get_mcp_server():
    return __setting.mcp_server


def get_data_base_dir():
    return DATA_BASE_DIR


def get_data_dir():
    return __setting.data_dir


def get_db_path():
    return os.path.join(CHROMA_BASE_DIR, __setting.model_provider)


def get_data_path(data: str = __setting.data_dir):
    return os.path.join(DATA_BASE_DIR, data)


def get_uploaded_data_path():
    return os.path.join(DATA_BASE_DIR, UPLOADED_DATA_DIR)


def get_data_file_path(data_dir: str, filename: str):
    return os.path.join(get_data_path(data_dir), filename)


def get_uploaded_data_file_path(filename: str):
    return os.path.join(get_uploaded_data_path(), filename)


def get_storage_path(data_dir: str, embed_model_name: str) -> str:
    return os.path.join(
        STORAGE_BASE_DIR, __setting.model_provider, data_dir, embed_model_name
    )


if __name__ == "__main__":
    print(get_config())
