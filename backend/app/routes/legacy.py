import os
from fastapi import APIRouter, Request, status
from fastapi.responses import FileResponse

from engine import vector_db, data_store, config, models, queryer, chatter

legacy = APIRouter()


@legacy.post("/{data}/query", tags=["legacy"])
async def query_index(data: str, request: Request):
    raw_data = await request.body()
    query = raw_data.decode("utf-8")
    return queryer.query(data, query)


@legacy.get("/{data}/get/{id}", tags=["legacy"])
def get_data_text(data, id):
    vector_texts = vector_db.get_vector_text(data, [id])
    text = vector_texts[0] if vector_texts else ""
    return {"text": text}


@legacy.get("/{data}/files/{filename}", tags=["legacy"])
def download_file(data, filename):
    data_dir = os.path.abspath(os.path.join(config.data_base_dir, data))
    print(data_dir)
    return FileResponse(path=data_dir, filename=filename)


@legacy.get("/data", tags=["legacy"])
def query_data():
    return data_store.get_data_names()


@legacy.get("/data_config", tags=["legacy"])
def get_data_config():
    return data_store.get_data_config()


@legacy.put("/data_config", tags=["legacy"], status_code=status.HTTP_204_NO_CONTENT)
async def update_data_config(request: Request):
    data_config = await request.json()
    data_store.update_data_config(data_config)


@legacy.get("/config", tags=["legacy"])
def get_config():
    return config.get_config()


@legacy.put("/config", tags=["legacy"], status_code=status.HTTP_204_NO_CONTENT)
async def update_config(request: Request):
    conf = await request.json()
    config.update_config(conf)


@legacy.get("/model_provider", tags=["legacy"])
def get_model_providers():
    return models.get_model_providers()


@legacy.get("/model_provider/{model_provider}", tags=["legacy"])
def get_model_config(model_provider):
    return models.get_model_config(model_provider)


@legacy.put(
    "/model_provider/{model_provider}",
    tags=["legacy"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_model_config(model_provider, request: Request):
    conf = await request.json()
    models.update_model_config(model_provider, conf)
    queryer.setStale(model_provider)
    chatter.setStale(model_provider)


@legacy.get("/embed_models", tags=["legacy"])
async def get_embed_models(reload):
    return models.get_models("embed", reload == "true")


@legacy.get("/chat_models", tags=["legacy"])
async def get_chat_models(reload):
    return models.get_models("chat", reload == "true")
