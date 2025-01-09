from app.engine import common, models, engines, caches


def chat(data_name: str, messages: models.ChatMessages):
    common.print_info(data_name)
    engine = engines.get_chat_engine(data_name)
    return engine.astream_chat(messages.last, messages.history)


def setStale(model_provider: str):
    caches.invalidate(model_provider)


if __name__ == "__main__":
    import sys, asyncio
    from app.engine import data_store, events

    data_name = len(sys.argv) >= 2 and sys.argv[1] or data_store.get_data_names()[0]
    question = (
        len(sys.argv) >= 3 and sys.argv[2] or data_store.get_default_question(data_name)
    )
    messages = models.ChatMessages([{"role": "user", "content": question}])

    async def asyncio_run():
        response = await chat(data_name, messages)
        async for event in events.event_handler.async_event_gen():
            print("event:", event)
        print("-" * 80)
        async for chunk in response.async_response_gen():
            print(chunk, end="")
        print("\n", "-" * 80, sep="")

    asyncio.run(asyncio_run())
