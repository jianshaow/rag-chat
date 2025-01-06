from llama_index.core.base.response.schema import Response

from engine import common, engines


def query(data_name: str, query_text: str):
    common.print_info(data_name)
    query_engine = engines.get_query_engine(data_name)
    response: Response = query_engine.query(query_text)
    sources = [
        {"id": node.node_id, "file_name": node.metadata["file_name"]}
        for node in response.source_nodes
    ]

    return {"text": str(response), "sources": sources}


def setStale(model_provider: str):
    engines.setStale(model_provider)


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
