import os
from dotenv import load_dotenv

load_dotenv()


data_base_dir = os.environ.get("DATA_BASE_DIR", "data")
chroma_base_dir = os.environ.get("CHROMA_BASE_DIR", "chroma")
api_spec = os.environ.get("API_SPEC", "ollama")


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
