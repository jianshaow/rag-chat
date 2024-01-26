from engine import config, indexer


def query(data_name=config.default_data_name, query_text=config.get_question()):
    query_engine = indexer.get_index(data_name).as_query_engine()
    response = query_engine.query(query_text)
    return str(response)


if __name__ == "__main__":
    answer = query()
    print(answer)
