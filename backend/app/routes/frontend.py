import json

from llama_index.core.chat_engine.types import StreamingAgentChatResponse

from app import backend_base_url


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
                    "url": backend_base_url
                    + "/api/en_novel/files/"
                    + (node.node.metadata.get("file_name") or ""),
                }
                for node in response.source_nodes
            ]
        },
    }
    return sources_data
