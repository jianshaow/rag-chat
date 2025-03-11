from fastapi import APIRouter, Request
from llama_index.core.base.response.schema import Response

from app.api.routes.payload import QueryResult, SourceNode
from app.api.routes.vercel import VercelStreamingResponse
from app.engine import engines, setting

query_router = r = APIRouter()


@r.post("", tags=["query"])
async def query_index(request: Request) -> QueryResult:
    raw_request = await request.body()
    query = raw_request.decode("utf-8")
    data = setting.get_data_dir()
    query_engine, _ = engines.get_query_engine(data)
    response: Response = query_engine.query(query)
    sources = [
        SourceNode(
            id=node.node_id,
            data_dir=node.metadata["data_dir"],
            file_name=node.metadata["file_name"],
        )
        for node in response.source_nodes
    ]
    return QueryResult(text=str(response), sources=sources)


@r.post("/stream", tags=["query"])
async def stream_query(request: Request):
    raw_request = await request.body()
    query = raw_request.decode("utf-8")
    data = setting.get_data_dir()
    query_engine, handler = engines.get_query_engine(data)
    response = query_engine.aquery(query)
    return VercelStreamingResponse.from_query_response(response, handler)
