from engine import config, indexer


def query(data_name, query_text=config.default_question):
    query_engine = indexer.get_index(data_name).as_query_engine()
    response = query_engine.query(query_text)
    return str(response)


if __name__ == "__main__":
    import sys
    from engine import data_store

    data_name = len(sys.argv) >= 2 and sys.argv[1] or data_store.get_data_names()[0]
    question = (
        len(sys.argv) >= 3 and sys.argv[2] or data_store.get_default_question(data_name)
    )
    answer = query(data_name=data_name, query_text=question)
    print(answer)
