from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.chat_engine.types import BaseChatEngine

from engine import indexer, models, caches


def get_query_engine(data_name: str) -> BaseQueryEngine:
    def as_query_engine() -> BaseQueryEngine:
        chat_model = models.get_chat_model()
        return indexer.get_index(data_name).as_query_engine(llm=chat_model)

    return caches.get_query_engine(as_query_engine)


def get_chat_engine(data_name: str) -> BaseChatEngine:
    def as_chat_engine() -> BaseChatEngine:
        chat_model = models.get_chat_model()
        return indexer.get_index(data_name).as_chat_engine(llm=chat_model)

    return caches.get_chat_engine(as_chat_engine)
