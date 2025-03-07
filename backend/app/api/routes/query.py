from fastapi import APIRouter, Request
from llama_index.core.base.response.schema import Response

from app.engine import engines

query_router = r = APIRouter()


@r.post("/{data}/query", tags=["query"])
async def query_index(data: str, request: Request):
    raw_data = await request.body()
    query = raw_data.decode("utf-8")
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
