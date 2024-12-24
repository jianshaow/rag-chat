from llama_index.core.base.response.schema import Response, StreamingResponse
from llama_index.core.tools.query_engine import BaseQueryEngine, QueryEngineTool
from llama_index.core.agent import AgentRunner

from engine import config, indexer, models, agents

__engines: dict[str, dict[str, BaseQueryEngine]] = {}
__agents: dict[str, dict[str, AgentRunner]] = {}


def query(data_name: str, query_text: str):
    model_provider = config.model_provider

    engines = __engines.get(model_provider, {})
    query_engine = engines.get(data_name)
    if query_engine is None:
        chat_model = models.new_model(config.model_provider, "chat")
        query_engine = indexer.get_index(data_name).as_query_engine(llm=chat_model)
        print("chat_model:", chat_model.model)
        engines[data_name] = query_engine
        __engines[model_provider] = engines

    response: Response = query_engine.query(query_text)
    sources = [
        {"id": node.node_id, "file_name": node.metadata["file_name"]}
        for node in response.source_nodes
    ]
    return {"text": str(response), "sources": sources}


def stream_query(data_name: str, messages: models.ChatMessages):
    print(messages)
    model_provider = config.model_provider

    engine_dict = __engines.get(model_provider, {})
    query_engine = engine_dict.get(data_name)
    agent_dict = __agents.get(model_provider, {})
    agent = agent_dict.get(data_name)
    if agent is None:
        chat_model = models.new_model(config.model_provider, "chat")
        query_engine = indexer.get_index(data_name).as_query_engine(llm=chat_model)
        print("chat_model:", chat_model.model)
        engine_dict[data_name] = query_engine
        tools = [QueryEngineTool.from_defaults(query_engine)]
        agent = agents.new_agent(chat_model, tools)
        agent_dict[data_name] = agent
        __engines[model_provider] = engine_dict
        __agents[model_provider] = agent_dict

    response: StreamingResponse = agent.stream_chat(messages.last, messages.history)
    return response


def setStale(model_provider: str):
    __engines.pop(model_provider, None)


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
