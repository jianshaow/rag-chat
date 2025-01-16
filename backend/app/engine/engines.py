from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.vector_stores.types import MetadataFilters

from app.engine import indexes, models, utils


def get_query_engine(data_dir: str) -> BaseQueryEngine:
    utils.print_info(data_dir)
    chat_model = models.get_chat_model()
    return indexes.get_index(data_dir).as_query_engine(llm=chat_model)


def get_chat_engine(data_dir: str, filters: MetadataFilters) -> BaseChatEngine:
    utils.print_info(data_dir)
    chat_model = models.get_chat_model()
    return indexes.get_index(data_dir).as_chat_engine(llm=chat_model, filters=filters)
