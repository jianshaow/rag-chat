import json, asyncio
from typing import Any, AsyncGenerator

from llama_index.core.callbacks.base_handler import BaseCallbackHandler
from llama_index.core.callbacks.schema import CBEventType
from llama_index.core.tools.types import ToolOutput


class CallbackEvent:

    def __init__(
        self,
        event_id: str,
        event_type: CBEventType,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self.event_id = event_id
        self.event_type = event_type
        self.payload = payload

    def to_response(self) -> dict | None:
        match self.event_type:
            case CBEventType.RETRIEVE:
                return self.get_retrieval_message()
            case CBEventType.FUNCTION_CALL:
                return self.get_tool_message()
            case CBEventType.AGENT_STEP:
                return self.get_agent_tool_response()
            case _:
                return None

    def get_retrieval_message(self) -> dict | None:
        if self.payload:
            nodes = self.payload.get("nodes")
            if nodes:
                msg = f"Retrieved {len(nodes)} sources to use as context for the query"
            else:
                msg = f"Retrieving context for query: '{self.payload.get('query_str')}'"
            return {
                "type": "events",
                "data": {"title": msg},
            }
        else:
            return None

    def get_tool_message(self) -> dict | None:
        if self.payload is None:
            return None
        func_call_args = self.payload.get("function_call")
        if func_call_args is not None and "tool" in self.payload:
            tool = self.payload.get("tool")
            if tool is None:
                return None
            return {
                "type": "events",
                "data": {
                    "title": f"Calling tool: {tool.name} with inputs: {func_call_args}",
                },
            }
        return None

    def get_agent_tool_response(self) -> dict | None:
        if self.payload is None:
            return None
        response = self.payload.get("response")
        if response is not None:
            sources = response.sources
            for source in sources:
                # Return the tool response here to include the toolCall information
                if isinstance(source, ToolOutput):
                    if self._is_output_serializable(source.raw_output):
                        output = source.raw_output
                    else:
                        output = source.content

                    return {
                        "type": "tools",
                        "data": {
                            "toolOutput": {
                                "output": output,
                                "isError": source.is_error,
                            },
                            "toolCall": {
                                "id": None,  # There is no tool id in the ToolOutput
                                "name": source.tool_name,
                                "input": source.raw_input,
                            },
                        },
                    }
        return None

    def _is_output_serializable(self, output: Any) -> bool:
        try:
            json.dumps(output)
            return True
        except TypeError:
            return False


class EventCallbackHandler(BaseCallbackHandler):

    def __init__(
        self,
    ):
        self.queue = asyncio.Queue()
        self.is_done: bool = False
        ignored_events = [
            CBEventType.CHUNKING,
            CBEventType.NODE_PARSING,
            CBEventType.EMBEDDING,
            CBEventType.LLM,
            CBEventType.TEMPLATING,
            CBEventType.AGENT_STEP,
        ]
        super().__init__(ignored_events, ignored_events)

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: dict[str, Any] | None = None,
        event_id: str = "",
        **kwargs,
    ) -> str:
        print("*" * 80)
        print("event", event_id, "start")
        print("event_type:", event_type)
        event = CallbackEvent(event_id=event_id, event_type=event_type, payload=payload)
        if response := event.to_response():
            print("response:", response)
            self.queue.put_nowait(event)
        print("*" * 80)
        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: dict[str, Any] | None = None,
        event_id: str = "",
        **kwargs,
    ) -> None:
        print("*" * 80)
        print("event", event_id, "end")
        print("event_type:", event_type)
        event = CallbackEvent(event_id=event_id, event_type=event_type, payload=payload)
        if response := event.to_response():
            print("response:", response)
            self.queue.put_nowait(event)
        print("*" * 80)

    def start_trace(self, trace_id: str | None = None) -> None:
        """No-op."""

    def end_trace(
        self,
        trace_id: str | None = None,
        trace_map: dict[str, list[str]] | None = None,
    ) -> None:
        """No-op."""

    async def async_event_gen(self) -> AsyncGenerator[CallbackEvent, None]:
        while not self.queue.empty() or not self.is_done:
            try:
                yield await asyncio.wait_for(self.queue.get(), timeout=0.1)
            except asyncio.TimeoutError:
                pass


event_handler = EventCallbackHandler()
