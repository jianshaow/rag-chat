import os, json
from app.engine import config


__default_data_config: dict = {
    "en_novel": {
        "data_dir": "en_novel",
        "data_type": "text",
        "default_question": "What did the author do growing up?",
    },
    "zh_novel": {
        "data_dir": "zh_novel",
        "data_type": "text",
        "default_question": "地球发动机都安装在哪里？",
    },
    "uploaded": {
        "data_dir": "uploaded",
        "data_type": "text",
        "default_question": "What is the document about?",
    },
}

__data_config: dict[str, dict[str, str]] = __default_data_config
data_config = os.environ.get("DATA_CONFIG")
if data_config and os.path.isfile(data_config):
    with open(data_config, "r") as file:
        __data_config = json.load(file)


def get_data_config():
    return __data_config


def update_data_config(data_config: dict):
    global __data_config
    __data_config = data_config


def get_data_path(data_dir: str):
    data_dir = os.path.join(
        config.data_base_dir, get_data_config()[data_dir]["data_dir"]
    )
    return data_dir


def get_default_question(data_name):
    return get_data_config()[data_name]["default_question"]


def get_data_dirs():
    return list(get_data_config().keys())


if __name__ == "__main__":
    data_config = get_data_config()
    print(data_config)
