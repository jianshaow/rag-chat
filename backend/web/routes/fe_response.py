import json

from llama_index.core.chat_engine.types import StreamingAgentChatResponse

from engine import backend_base_url


def get_sources(response: StreamingAgentChatResponse):
    sources = json.dumps(
        [
            {
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
        ]
    )
    return sources
