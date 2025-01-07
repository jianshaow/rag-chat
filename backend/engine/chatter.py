from llama_index.core.chat_engine.types import StreamingAgentChatResponse

from engine import common, models, agents, engines


def chat(data_name: str, messages: models.ChatMessages) -> StreamingAgentChatResponse:
    common.print_info(data_name)
    # return _chat_with_agent(data_name, messages)
    return _chat_with_engine(data_name, messages)


def setStale(model_provider: str):
    agents.setStale(model_provider)


def _chat_with_agent(data_name: str, messages: models.ChatMessages):
    agent = agents.get_agent(data_name)
    return agent.stream_chat(messages.last, messages.history)


def _chat_with_engine(data_name: str, messages: models.ChatMessages):
    engine = engines.get_chat_engine(data_name)
    return engine.stream_chat(messages.last, messages.history)


if __name__ == "__main__":
    import sys
    from engine import data_store

    data_name = len(sys.argv) >= 2 and sys.argv[1] or data_store.get_data_names()[0]
    question = (
        len(sys.argv) >= 3 and sys.argv[2] or data_store.get_default_question(data_name)
    )
    messages = models.ChatMessages([{"role": "user", "content": question}])
    response = chat(data_name, messages)
    print("-" * 80)
    for chunk in response.response_gen:
        print(chunk, end="")
    print("\n", "-" * 80, sep="")
