import os

from engine import data_base_dir, chroma_base_dir, api_spec


def get_db_path():
    return os.path.join(chroma_base_dir, api_spec)


def get_config():
    return {
        "data_base_dir": data_base_dir,
        "chroma_base_dir": chroma_base_dir,
        "api_spec": api_spec,
    }


def update_config(conf: dict):
    global data_base_dir, chroma_base_dir, api_spec
    data_base_dir = conf.get("data_base_dir", data_base_dir)
    chroma_base_dir = conf.get("chroma_base_dir", chroma_base_dir)
    api_spec = conf.get("api_spec", api_spec)


if __name__ == "__main__":
    print(get_config())
