from typing import Tuple

from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.vector_stores.types import MetadataFilters

from app.engine import events, indexes, models, utils


def get_query_engine(
    data_dir: str,
) -> Tuple[BaseQueryEngine, events.QueueEventCallbackHandler]:
    utils.log_model_info(data_dir)
    chat_model = models.get_chat_model()
    index, context = indexes.get_index(data_dir)
    return (
        index.as_query_engine(llm=chat_model, streaming=True, verbose=True),
        context.get(),
    )


def get_chat_engine(
    data_dir: str, filters: MetadataFilters
) -> Tuple[BaseChatEngine, events.QueueEventCallbackHandler]:
    utils.log_model_info(data_dir)
    chat_model = models.get_chat_model()
    index, context = indexes.get_index(data_dir)
    return (
        index.as_chat_engine(llm=chat_model, filters=filters, verbose=True),
        context.get(),
    )
