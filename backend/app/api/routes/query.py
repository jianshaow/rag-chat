from fastapi import APIRouter, Request
from llama_index.core.base.response.schema import Response
from llama_index.core.vector_stores.types import MetadataFilters

from app.api.routes.payload import QueryResult, SourceNode
from app.api.routes.vercel import VercelStreamingResponse
from app.engine import agents, engines, setting

query_router = r = APIRouter()


@r.post("", tags=["query"])
async def query_index(request: Request) -> QueryResult:
    raw_request = await request.body()
    query = raw_request.decode("utf-8")
    data = setting.get_data_dir()
    query_engine, _ = engines.get_query_engine(data, streaming=False)
    response: Response = query_engine.query(query)  # type: ignore
    return QueryResult(
        answer=str(response),
        sources=SourceNode.from_source_nodes(response.source_nodes),
    )


@r.post("/stream", tags=["query"])
async def stream_query(request: Request):
    raw_request = await request.body()
    query = raw_request.decode("utf-8")
    data = setting.get_data_dir()
    query_engine, handler = engines.get_query_engine(data)
    response = query_engine.aquery(query)
    return VercelStreamingResponse.from_query_response(response, handler)  # type: ignore


@r.post("/agent_stream", tags=["query"])
async def agent_stream_query(request: Request):
    raw_request = await request.body()
    query = raw_request.decode("utf-8")
    data = setting.get_data_dir()
    agent = await agents.get_agent(data, MetadataFilters(filters=[]))
    response = agent.run(query)
    return VercelStreamingResponse.from_agent_response(response)
