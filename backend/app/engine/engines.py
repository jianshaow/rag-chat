from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.chat_engine.types import BaseChatEngine

from . import indexer, models, caches, utils


def get_query_engine(data_name: str) -> BaseQueryEngine:
    utils.print_info(data_name)
    def as_query_engine() -> BaseQueryEngine:
        chat_model = models.get_chat_model()
        return indexer.get_index(data_name).as_query_engine(llm=chat_model)

    return caches.get_query_engine(as_query_engine)


def get_chat_engine(data_name: str) -> BaseChatEngine:
    utils.print_info(data_name)
    def as_chat_engine() -> BaseChatEngine:
        chat_model = models.get_chat_model()
        return indexer.get_index(data_name).as_chat_engine(llm=chat_model)

    return caches.get_chat_engine(as_chat_engine)
