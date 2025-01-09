from llama_index.core.chat_engine.types import StreamingAgentChatResponse

from app.api import files_base_url

data_name = "en_novel"
file_dir = f"{files_base_url}/{data_name}"


def extract_sources_data(response: StreamingAgentChatResponse):
    sources_data = {
        "type": "sources",
        "data": {
            "nodes": [
                {
                    "id": node.node_id,
                    "metadata": node.node.metadata,
                    "score": node.score,
                    "text": node.text,
                    "url": f"{file_dir}/{(node.node.metadata.get("file_name") or "")}",
                }
                for node in response.source_nodes
            ]
        },
    }
    return sources_data
