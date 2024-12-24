import os

from engine import data_base_dir, chroma_base_dir, model_provider


def get_db_path():
    return os.path.join(chroma_base_dir, model_provider)


def get_config():
    return {
        "data_base_dir": data_base_dir,
        "chroma_base_dir": chroma_base_dir,
        "model_provider": model_provider,
    }


def update_config(conf: dict):
    global data_base_dir, chroma_base_dir, model_provider
    data_base_dir = conf.get("data_base_dir", data_base_dir)
    chroma_base_dir = conf.get("chroma_base_dir", chroma_base_dir)
    model_provider = conf.get("model_provider", model_provider)


if __name__ == "__main__":
    print(get_config())
