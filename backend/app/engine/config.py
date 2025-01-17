import os

from app.engine import data_base_dir, data_dir, chroma_base_dir, model_provider


def get_db_path():
    return os.path.join(chroma_base_dir, model_provider)


def get_data_path(data: str = data_dir):
    return os.path.join(data_base_dir, data)


def get_data_file_path(data: str, filename: str):
    return os.path.join(get_data_path(data), filename)


def get_config():
    return {
        "data_base_dir": data_base_dir,
        "data_dir": data_dir,
        "chroma_base_dir": chroma_base_dir,
        "model_provider": model_provider,
    }


def update_config(conf: dict):
    global data_base_dir, data_dir, chroma_base_dir, model_provider
    data_base_dir = conf.get("data_base_dir", data_base_dir)
    data_dir = conf.get("data_dir", data_dir)
    chroma_base_dir = conf.get("chroma_base_dir", chroma_base_dir)
    model_provider = conf.get("model_provider", model_provider)


if __name__ == "__main__":
    print(get_config())
