from llama_index.core.llms import LLM
from llama_index.core.agent import AgentRunner
from llama_index.core.tools.query_engine import BaseQueryEngine, QueryEngineTool

from engine import config, indexer, models

__agents: dict[str, AgentRunner] = {}


def new_agent(llm: LLM, tools) -> AgentRunner:
    return AgentRunner.from_llm(llm=llm, tools=tools)


def get_agent(data_name: str) -> AgentRunner:
    model_provider = config.model_provider
    agent_key = f"{data_name}@{model_provider}"
    agent = __agents.get(agent_key)
    if agent is None:
        chat_model = models.new_model(config.model_provider, "chat")
        query_engine = indexer.get_index(data_name).as_query_engine(llm=chat_model)
        tools = [QueryEngineTool.from_defaults(query_engine)]
        agent = new_agent(chat_model, tools)
        __agents[agent_key] = agent

    return agent


def setStale(model_provider: str):
    __agents.pop(model_provider, None)
