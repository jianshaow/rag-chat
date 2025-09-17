from typing import Tuple

from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.tools import RetrieverTool
from llama_index.core.vector_stores.types import MetadataFilters

from app.engine import events, indexes, models, utils


def get_agent(
    data_dir: str, filters: MetadataFilters
) -> Tuple[AgentWorkflow, events.QueueEventCallbackHandler]:
    utils.log_model_info(data_dir)
    chat_model = models.get_chat_model()
    index, context = indexes.get_index(data_dir)
    retriever_tool = RetrieverTool.from_defaults(
        index.as_retriever(filters=filters, verbose=True)
    )
    agent = AgentWorkflow.from_tools_or_functions([retriever_tool], chat_model)
    return agent, context.get()
