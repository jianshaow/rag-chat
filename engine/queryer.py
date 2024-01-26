from engine import config, indexer


def query(query_text):
    query_engine = indexer.get_index().as_query_engine()
    response = query_engine.query(query_text)
    return str(response)


if __name__ == "__main__":
    answer = query(config.get_question())
    print(answer)
