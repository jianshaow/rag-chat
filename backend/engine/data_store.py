import os, json
from engine import config


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
}

__data_config: dict = None


def get_data_config():
    global __data_config
    if __data_config is None:
        data_config = os.environ.get("DATA_CONFIG")
        if data_config:
            if os.path.isfile(data_config):
                with open(data_config, "r") as file:
                    __data_config = json.load(file)
        else:
            __data_config = __default_data_config
    return __data_config


def update_data_config(data_config: dict):
    global __data_config
    __data_config = data_config


def get_data_dir(data_name):
    data_dir = os.path.join(
        config.data_base_dir, get_data_config()[data_name]["data_dir"]
    )
    return data_dir


def get_data_type(data_name):
    return get_data_config()[data_name]["data_type"]


def get_default_question(data_name):
    return get_data_config()[data_name]["default_question"]


def get_data_names():
    return list(get_data_config().keys())


if __name__ == "__main__":
    data_config = get_data_config()
    print(data_config)
