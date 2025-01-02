from llama_index.core.tools.query_engine import BaseQueryEngine

from engine import config, indexer, models

__engines: dict[str, BaseQueryEngine] = {}


def get_query_engine(data_name: str) -> BaseQueryEngine:
    model_provider = config.model_provider
    engine_key = f"{data_name}@{model_provider}"
    query_engine = __engines.get(engine_key)

    if query_engine is None:
        chat_model = models.new_model(model_provider, "chat")
        query_engine = indexer.get_index(data_name).as_query_engine(llm=chat_model)
        __engines[engine_key] = query_engine

    return query_engine


def setStale(model_provider: str):
    __engines.pop(model_provider, None)
