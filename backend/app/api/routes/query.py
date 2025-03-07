from fastapi import APIRouter, Request
from llama_index.core.base.response.schema import Response

from app.engine import config, engines

query_router = r = APIRouter()


@r.post("", tags=["query"])
async def query_index(request: Request):
    raw_request = await request.body()
    query = raw_request.decode("utf-8")
    data = config.get_data_dir()
    query_engine, _ = engines.get_query_engine(data)
    response: Response = query_engine.query(query)
    sources = [
        {
            "id": node.node_id,
            "data_dir": node.metadata["data_dir"],
            "file_name": node.metadata["file_name"],
        }
        for node in response.source_nodes
    ]

    return {"text": str(response), "sources": sources}
