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


if __name__ == "__main__":
    scan_data_root_dir()
    print(__data_dir_dict)
