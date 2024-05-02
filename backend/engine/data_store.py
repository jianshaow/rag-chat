import os
from engine import config


__data_dir_dict: dict = None

__data_config = {
    "en_novel": {
        "data_dir": "en_novel",
        "default_question": "What did the author do growing up?",
    },
    "zh_novel": {
        "data_dir": "zh_novel",
        "default_question": "地球发动机都安装在哪里？",
    },
}


def scan_data_dirs():
    global __data_dir_dict
    __data_dir_dict = {}
    base_dir = config.data_base_dir
    for key, value in __data_config.items():
        data_dir = value["data_dir"]
        path = os.path.join(base_dir, data_dir)
        if os.path.isdir(path):
            __data_dir_dict[key] = path


def get_data_path(data_name):
    if __data_dir_dict is None:
        scan_data_dirs()
    return __data_dir_dict[data_name]


def get_default_question(data_name):
    return __data_config[data_name]["default_question"]


def get_data_names():
    return list(__data_config.keys())


if __name__ == "__main__":
    data_names = get_data_names()
    print(data_names)
