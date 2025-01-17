from llama_index.core.base.response.schema import Response
from fastapi import APIRouter, Request, status
from fastapi.responses import FileResponse

from app.engine import data_store, config, models, engines, caches, vectordb

legacy_router = r = APIRouter()


@r.post("/{data}/query", tags=["legacy"])
async def query_index(data: str, request: Request):
    raw_data = await request.body()
    query = raw_data.decode("utf-8")
    query_engine = engines.get_query_engine(data)
    response: Response = query_engine.query(query)
    sources = [
        {"id": node.node_id, "file_name": node.metadata["file_name"]}
        for node in response.source_nodes
    ]

    return {"text": str(response), "sources": sources}


@r.get("/{data}/get/{id}", tags=["legacy"])
def get_data_text(data, id):
    vector_texts = vectordb.get_doc_text(data, [id])
    text = vector_texts[0] if vector_texts else ""
    return {"text": text}


@r.get("/{data}/files/{filename}", tags=["legacy"])
def download_file(data, filename):
    path = config.get_data_file_path(data, filename)
    return FileResponse(path=path)


@r.get("/data", tags=["legacy"])
def query_data():
    return data_store.get_data_dirs()


@r.get("/data_config", tags=["legacy"])
def get_data_config():
    return data_store.get_data_config()


@r.put("/data_config", tags=["legacy"], status_code=status.HTTP_204_NO_CONTENT)
async def update_data_config(request: Request):
    data_config = await request.json()
    data_store.update_data_config(data_config)


@r.get("/config", tags=["legacy"])
def get_config():
    return config.get_config()


@r.put("/config", tags=["legacy"], status_code=status.HTTP_204_NO_CONTENT)
async def update_config(request: Request):
    conf = await request.json()
    config.update_config(conf)


@r.get("/model_provider", tags=["legacy"])
def get_model_providers():
    return models.get_model_providers()


@r.get("/model_provider/{model_provider}", tags=["legacy"])
def get_model_config(model_provider):
    return models.get_model_config(model_provider)


@r.put(
    "/model_provider/{model_provider}",
    tags=["legacy"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_model_config(model_provider, request: Request):
    conf = await request.json()
    models.update_model_config(model_provider, conf)
    caches.invalidate(model_provider)


@r.get("/embed_models", tags=["legacy"])
def get_embed_models(reload):
    return models.get_models("embed", reload == "true")


@r.get("/chat_models", tags=["legacy"])
def get_chat_models(reload):
    return models.get_models("chat", reload == "true")
