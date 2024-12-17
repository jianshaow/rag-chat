from llama_index.core.base.response.schema import Response, StreamingResponse
from llama_index.core.tools.query_engine import BaseQueryEngine, QueryEngineTool
from llama_index.core.agent import AgentRunner

from engine import config, indexer, models, agents

__engines: dict[str, dict[str, BaseQueryEngine]] = {}
__agents: dict[str, dict[str, AgentRunner]] = {}


def query(data_name: str, query_text: str):
    api_spec = config.api_spec

    engines = __engines.get(api_spec, {})
    query_engine = engines.get(data_name)
    if query_engine is None:
        chat_model = models.new_model(config.api_spec, "chat")
        query_engine = indexer.get_index(data_name).as_query_engine(llm=chat_model)
        print("chat_model:", chat_model.model)
        engines[data_name] = query_engine
        __engines[api_spec] = engines

    response: Response = query_engine.query(query_text)
    sources = [
        {"id": node.node_id, "file_name": node.metadata["file_name"]}
        for node in response.source_nodes
    ]
    return {"text": str(response), "sources": sources}


def stream_query(data_name: str, messages: models.ChatMessages):
    print(messages)
    api_spec = config.api_spec

    engine_dict = __engines.get(api_spec, {})
    query_engine = engine_dict.get(data_name)
    agent_dict = __agents.get(api_spec, {})
    agent = agent_dict.get(data_name)
    if agent is None:
        chat_model = models.new_model(config.api_spec, "chat")
        query_engine = indexer.get_index(data_name).as_query_engine(llm=chat_model)
        print("chat_model:", chat_model.model)
        engine_dict[data_name] = query_engine
        tools = [QueryEngineTool.from_defaults(query_engine)]
        agent = agents.new_agent(chat_model, tools)
        agent_dict[data_name] = agent
        __engines[api_spec] = engine_dict
        __agents[api_spec] = agent_dict

    response: StreamingResponse = agent.stream_chat(messages.last, messages.history)
    return response.response_gen


def setStale(api_spec: str):
    __engines.pop(api_spec, None)


if __name__ == "__main__":
    import sys
    from engine import data_store

    data_name = len(sys.argv) >= 2 and sys.argv[1] or data_store.get_data_names()[0]
    question = (
        len(sys.argv) >= 3 and sys.argv[2] or data_store.get_default_question(data_name)
    )
    answer = query(data_name, question)
    print("-" * 80)
    print(answer)
    print("-" * 80)
