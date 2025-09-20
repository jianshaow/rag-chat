import os
from typing import Dict

import yaml
from pydantic import BaseModel, RootModel

from app.engine import UPLOADED_DATA_DIR, setting


class DataConfig(BaseModel):
    default_question: str


class DataConfigs(RootModel[Dict[str, DataConfig]]):

    def __getitem__(self, key: str) -> DataConfig:
        return self.root[key]

    def keys(self):
        return self.root.keys()

    def items(self):
        return self.root.items()

    def values(self):
        return self.root.values()


DEFAULT_DATA_CONFIG = DataConfig(default_question="What is the document about?")


__builtin_data_config = DataConfigs.model_validate(
    {
        "en_novel": DataConfig(default_question="What did the author do growing up?"),
        "zh_novel": DataConfig(default_question="地球发动机都安装在哪里？"),
    }
)

__data_configs: DataConfigs = __builtin_data_config

data_config_file = os.environ.get(
    "DATA_CONFIG", os.path.join(setting.get_data_base_dir(), "data_config.yaml")
)

if data_config_file and os.path.isfile(data_config_file):
    with open(data_config_file, "r", encoding="utf-8") as file:
        __data_configs.root.update(yaml.safe_load(file))


def get_data_config():
    data_config: dict[str, DataConfig] = {}
    data_base_dir = setting.get_data_base_dir()
    if os.path.exists(data_base_dir) and os.path.isdir(data_base_dir):
        data_dirs = os.listdir(data_base_dir)
        for data_dir in data_dirs:
            if data_dir != UPLOADED_DATA_DIR and os.path.isdir(
                os.path.join(data_base_dir, data_dir)
            ):
                data_config[data_dir] = (
                    __data_configs[data_dir]
                    if data_dir in __data_configs.keys()
                    else DEFAULT_DATA_CONFIG
                )
    return data_config


def get_data_path(data_dir: str):
    return setting.get_data_path(data_dir)


def get_default_question(data_dir):
    return get_data_config()[data_dir].default_question


def get_data_dirs() -> list[str]:
    return list(get_data_config().keys())


if __name__ == "__main__":
    curent_data_config = get_data_config()
    print(curent_data_config)
