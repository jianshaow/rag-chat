from llama_index.core.tools.query_engine import QueryEngineTool
from engine import config, indexer, models, agents

__engines = {}


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

    response = query_engine.query(query_text)
    sources = [
        {"id": node.node_id, "file_name": node.metadata["file_name"]}
        for node in response.source_nodes
    ]
    return {"text": str(response), "sources": sources}


def stream_query(data_name: str, query_text: str):
    api_spec = config.api_spec

    engines = __engines.get(api_spec, {})
    query_engine = engines.get(data_name)
    if query_engine is None:
        chat_model = models.new_model(config.api_spec, "chat")
        query_engine = indexer.get_index(data_name).as_query_engine(llm=chat_model)
        print("chat_model:", chat_model.model)
        engines[data_name] = query_engine
        __engines[api_spec] = engines

    tools = [QueryEngineTool.from_defaults(query_engine)]
    agent = agents.get_agent(chat_model, tools)

    return agent.stream_chat(query_text)


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
