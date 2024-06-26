from engine import config, indexer, models

__engines = {}


def query(data_name, query_text):
    engine_key = "{data_name}@{model_spec}".format(
        data_name=data_name, model_spec=config.api_spec
    )
    query_engine = __engines.get(engine_key)
    if query_engine is None:
        chat_model = models.new_model("chat")
        query_engine = indexer.get_index(data_name).as_query_engine(llm=chat_model)
        print("chat_model:", chat_model.model)
        __engines[engine_key] = query_engine

    response = query_engine.query(query_text)
    return str(response)


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
