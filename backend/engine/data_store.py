import os
from engine import config


__data_dir_dict: dict = None


def scan_data_root_dir():
    global __data_dir_dict
    __data_dir_dict = {}
    root = config.data_root_dir
    __data_dir_dict[config.default_data_name] = root
    for entry in os.listdir(config.data_root_dir):
        path = os.path.join(root, entry)
        if os.path.isdir(path):
            __data_dir_dict[entry] = path


def get_data_path(data_name):
    if __data_dir_dict is None:
        scan_data_root_dir()
    return __data_dir_dict[data_name]


def get_all_data_path():
    if __data_dir_dict is None:
        scan_data_root_dir()
    return {
        key: value
        for key, value in __data_dir_dict.items()
        if key != config.default_data_name
    }


if __name__ == "__main__":
    data_path = get_all_data_path()
    print(data_path)
