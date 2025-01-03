from llama_index.core.base.response.schema import StreamingResponse

from engine import common, models, agents


def chat(data_name: str, messages: models.ChatMessages) -> StreamingResponse:
    agent = agents.get_agent(data_name)

    common.print_info(data_name)
    return agent.stream_chat(messages.last, messages.history)


def setStale(model_provider: str):
    agents.setStale(model_provider)


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
