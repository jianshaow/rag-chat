from llama_index.core.llms import LLM
from llama_index.core.agent import AgentRunner


def new_agent(llm: LLM, tools):
    return AgentRunner.from_llm(llm=llm, tools=tools)
