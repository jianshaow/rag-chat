from typing import Callable, Coroutine, List, Tuple, Union, cast

from llama_index.core.agent.workflow import AgentStream, AgentWorkflow
from llama_index.core.llms import LLM
from llama_index.core.settings import Settings
from llama_index.core.vector_stores.types import MetadataFilters
from llama_index.core.workflow import Context
from workflows.events import Event

from app.engine import events, indexes, models, tools, utils

FINAL_ANSWER_PREFIX = "Answer: "


class ReActContext(Context):
    def __init__(self, *args, **kwargs):
        self.buffer = ""
        self.started = False
        self.final_answer = ""
        super().__init__(*args, **kwargs)

    def write_event_to_stream(self, ev: Event | None) -> None:
        if ev is None:
            return
        if isinstance(ev, AgentStream):
            if self.started:
                self.final_answer += ev.delta
                ev.response = self.final_answer
                super().write_event_to_stream(ev)
            else:
                self.buffer += ev.delta
                if FINAL_ANSWER_PREFIX in self.buffer:
                    self.started = True
                    ev.delta = self.buffer.split(FINAL_ANSWER_PREFIX)[-1]
                    ev.response = self.final_answer = ev.delta
                    super().write_event_to_stream(ev)

        else:
            self.buffer = ""
            self.started = False
            self.final_answer = ""
            super().write_event_to_stream(ev)


class FunctionContext(Context):
    def write_event_to_stream(self, ev: Event | None) -> None:
        if ev is None:
            return
        if isinstance(ev, AgentStream):
            if ev.response != "":
                super().write_event_to_stream(ev)
        else:
            super().write_event_to_stream(ev)


def from_tools_or_functions(*args, **kwargs) -> AgentWorkflow:
    agent = AgentWorkflow.from_tools_or_functions(*args, **kwargs)

    llm = args[1] or kwargs.get("llm") or Settings.llm
    llm = cast(LLM, llm)
    if llm.metadata.is_function_calling_model:
        ctx = FunctionContext(agent)
    else:
        ctx = ReActContext(agent)

    def wrap_run(func):
        def wrapper(*args, **kwargs):
            return func(ctx=ctx, *args, **kwargs)

        return wrapper

    agent.run = wrap_run(agent.run)
    return agent


async def get_agent(
    data_dir: str, filters: MetadataFilters
) -> Tuple[AgentWorkflow, events.QueueEventCallbackHandler]:
    utils.log_model_info(data_dir)
    chat_model = models.get_chat_model()
    tool_set = tools.get_tool_set()
    if tool_set:
        _tools = await tool_set.get_tools(filters)
        return (
            from_tools_or_functions(_tools, chat_model),
            indexes.contextvar_event_handler.context.get(),
        )
    else:
        return (
            from_tools_or_functions(llm=chat_model),
            indexes.contextvar_event_handler.context.get(),
        )
