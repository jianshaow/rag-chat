import os
from engine import config


__data_dir_dict: dict = None


def scan_data_base_dir():
    global __data_dir_dict
    __data_dir_dict = {}
    root = config.data_base_dir
    for entry in os.listdir(config.data_base_dir):
        path = os.path.join(root, entry)
        if os.path.isdir(path):
            __data_dir_dict[entry] = path


def get_data_path(data_name):
    if __data_dir_dict is None:
        scan_data_base_dir()
    return __data_dir_dict[data_name]


def get_data_names():
    if __data_dir_dict is None:
        scan_data_base_dir()
    return list(__data_dir_dict.keys())


if __name__ == "__main__":
    data_path = get_data_names()
    print(data_path)
