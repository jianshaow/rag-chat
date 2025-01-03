from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.chat_engine.types import BaseChatEngine

from engine import config, indexer, models

__query_engines: dict[str, BaseQueryEngine] = {}
__chat_engines: dict[str, BaseChatEngine] = {}


def get_query_engine(data_name: str) -> BaseQueryEngine:
    model_provider = config.model_provider
    engine_key = f"{data_name}@{model_provider}"
    query_engine = __query_engines.get(engine_key)

    if query_engine is None:
        chat_model = models.new_model(model_provider, "chat")
        query_engine = indexer.get_index(data_name).as_query_engine(llm=chat_model)
        __query_engines[engine_key] = query_engine

    return query_engine


def get_chat_engine(data_name: str) -> BaseChatEngine:
    model_provider = config.model_provider
    engine_key = f"{data_name}@{model_provider}"
    chat_engine = __chat_engines.get(engine_key)

    if chat_engine is None:
        chat_model = models.new_model(model_provider, "chat")
        chat_engine = indexer.get_index(data_name).as_chat_engine(llm=chat_model)
        __chat_engines[engine_key] = chat_engine

    return chat_engine


def setStale(model_provider: str):
    __query_engines.pop(model_provider, None)
    __chat_engines.pop(model_provider, None)
