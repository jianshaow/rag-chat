import logging

from fastapi import APIRouter, status

from app.engine import data_store, indexes, vectordb
from app.engine.data_store import DataConfig

logger = logging.getLogger(__name__)

data_router = r = APIRouter()


@r.get("", tags=["data"])
async def query_data() -> list[str]:
    return data_store.get_data_dirs()


@r.post("/{data}", tags=["data"], status_code=status.HTTP_204_NO_CONTENT)
async def ingest_data(data) -> None:
    indexes.index_data(data)


@r.get("/{data}/node/{node_id}", tags=["data"])
async def get_data_text(data, node_id) -> dict[str, str]:
    vector_texts = vectordb.get_doc_text(data, [node_id])
    text = vector_texts[0] if vector_texts else ""
    return {"text": text}


@r.get("/config", tags=["data"])
async def get_data_config() -> dict[str, DataConfig]:
    return data_store.get_data_config()
