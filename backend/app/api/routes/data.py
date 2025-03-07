import logging

from fastapi import APIRouter

from app.engine import data_store, vectordb

logger = logging.getLogger(__name__)

data_router = r = APIRouter()


@r.get("", tags=["data"])
def query_data():
    return data_store.get_data_dirs()


@r.get("/{data}/node/{node_id}", tags=["data"])
def get_data_text(data, node_id):
    vector_texts = vectordb.get_doc_text(data, [node_id])
    text = vector_texts[0] if vector_texts else ""
    return {"text": text}


@r.get("/config", tags=["data"])
def get_data_config():
    return data_store.get_data_config()
