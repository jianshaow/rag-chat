import os

data_base_dir = os.environ.get("DATA_BASE_DIR", "data")
chroma_base_dir = os.environ.get("CHROMA_BASE_DIR", "chroma")
model_spec = os.environ.get("MODEL_SPEC", "openai")


def get_db_path():
    return os.path.join(chroma_base_dir, model_spec)


def get_config():
    return {
        "data_base_dir": data_base_dir,
        "chroma_base_dir": chroma_base_dir,
        "model_spec": model_spec,
    }


def update_config(conf: dict):
    global data_base_dir, chroma_base_dir, model_spec
    data_base_dir = conf.get("data_base_dir", data_base_dir)
    chroma_base_dir = conf.get("chroma_base_dir", chroma_base_dir)
    model_spec = conf.get("model_spec", model_spec)


if __name__ == "__main__":
    print(get_config())
