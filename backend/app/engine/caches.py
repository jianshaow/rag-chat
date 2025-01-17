from typing import Type, Any, Callable, TypeVar

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.llms import LLM
from llama_index.core import VectorStoreIndex

from app.engine import config

T = TypeVar("T", BaseEmbedding, LLM, VectorStoreIndex)

__cache: dict[str, dict[str, Any]] = {}


def get_embed_model(builder: Callable[..., BaseEmbedding]) -> BaseEmbedding:
    return get_from_cache(BaseEmbedding, builder)


def get_chat_model(builder: Callable[..., LLM]) -> LLM:
    return get_from_cache(LLM, builder)


def get_index(builder: Callable[..., VectorStoreIndex], key: str) -> VectorStoreIndex:
    return get_from_cache(VectorStoreIndex, builder, key=key)


def get_from_cache(cls: Type[T], builder: Callable[..., T], key: str = "") -> T:
    cache_bucket = get_cache_bucket()
    cache_key = f"{key}@{cls.__name__}"
    cache_item = cache_bucket.get(cache_key)
    if cache_item is None:
        cache_item = builder()
        cache_bucket[cache_key] = cache_item
    return cache_item


def get_cache_bucket() -> dict[str, Any]:
    model_provider = config.model_provider
    cache_bucket = __cache.get(model_provider)
    if cache_bucket is None:
        __cache[model_provider] = cache_bucket = {}
    return cache_bucket


def invalidate(model_provider: str):
    __cache.pop(model_provider, None)
