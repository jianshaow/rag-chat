from contextvars import ContextVar
from typing import Any, List, Tuple

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.callbacks import CallbackManager
from llama_index.core.callbacks.base_handler import BaseCallbackHandler
from llama_index.core.callbacks.schema import CBEventType
from llama_index.core.ingestion import DocstoreStrategy, IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Document
from llama_index.vector_stores.chroma import ChromaVectorStore

from app.engine import caches, data_store, events, loaders, models, setting, stores


class ContextVarEventCallbackHandler(BaseCallbackHandler):

    def __init__(self) -> None:
        ignored_events = [
            CBEventType.CHUNKING,
            CBEventType.NODE_PARSING,
            CBEventType.EMBEDDING,
            CBEventType.LLM,
            CBEventType.TEMPLATING,
            CBEventType.AGENT_STEP,
        ]
        super().__init__(ignored_events, ignored_events)
        self.handler_context: ContextVar[events.QueueEventCallbackHandler] = ContextVar(
            "handler_context"
        )

    @property
    def context(self) -> ContextVar[events.QueueEventCallbackHandler]:
        return self.handler_context

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: dict[str, Any] | None = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs,
    ) -> str:
        event_handler = self.handler_context.get(None)
        if event_handler:
            return event_handler.on_event_start(
                event_type, payload, event_id, parent_id, **kwargs
            )
        else:
            return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: dict[str, Any] | None = None,
        event_id: str = "",
        **kwargs,
    ) -> None:
        event_handler = self.handler_context.get(None)
        if event_handler:
            event_handler.on_event_end(event_type, payload, event_id, **kwargs)

    def start_trace(self, trace_id: str | None = None) -> None:
        event_handler = self.handler_context.get(None)
        if event_handler:
            event_handler.start_trace(trace_id)

    def end_trace(
        self,
        trace_id: str | None = None,
        trace_map: dict[str, list[str]] | None = None,
    ) -> None:
        event_handler = self.handler_context.get(None)
        if event_handler:
            event_handler.end_trace(trace_id, trace_map)


contextvar_event_handler = ContextVarEventCallbackHandler()


def ingest(documents: List[Document], data_dir: str):
    vector_store = stores.get_vector_store(data_dir)
    docstore = stores.get_docstore(
        setting.get_storage_path(data_dir, models.get_escaped_embed_model_name())
    )
    pipeline = IngestionPipeline(
        transformations=[SentenceSplitter(), models.get_embed_model()],
        docstore=docstore,
        vector_store=vector_store,
        docstore_strategy=DocstoreStrategy.UPSERTS_AND_DELETE,
    )
    nodes = pipeline.run(documents=documents, show_progress=True)
    StorageContext.from_defaults(docstore=docstore, vector_store=vector_store).persist(
        setting.get_storage_path(data_dir, models.get_escaped_embed_model_name())
    )
    return nodes


def index_data(data_dir: str):
    documents = loaders.load_doc_from_dir(data_dir)
    for doc in documents:
        doc.metadata["private"] = "false"
        doc.metadata["data_dir"] = data_dir
    return ingest(documents, data_dir)


def _load_index(vector_store: ChromaVectorStore) -> VectorStoreIndex:
    embed_model = models.get_embed_model()
    callback_manager = CallbackManager(
        [events.LogEventCallbackHandler(), contextvar_event_handler]
    )
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model,
        callback_manager=callback_manager,
        show_progress=True,
    )

    return index


def get_index(
    data_dir: str,
) -> Tuple[VectorStoreIndex, ContextVar[events.QueueEventCallbackHandler]]:
    embed_model_name = models.get_embed_model_name()
    index_key = f"{data_dir}@{embed_model_name}"
    vector_store = stores.get_vector_store(data_dir)
    index_builder = lambda: _load_index(vector_store)
    return caches.get_index(index_builder, index_key), contextvar_event_handler.context


def __retrieve_data(data_dir: str):
    question = data_store.get_default_question(data_dir)
    index, _ = get_index(data_dir)
    print("-" * 80)
    print("embed model:", index._embed_model.model_name)
    print("Question: ", question)
    retriever = index.as_retriever()
    nodes = retriever.retrieve(question)
    for node in nodes:
        print("-" * 80)
        print(node)


def _main():
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "index":
            data_dir = len(sys.argv) == 3 and sys.argv[2] or setting.get_data_dir()
            index_data(data_dir)
        elif sys.argv[1] == "retrieve":
            data_dir = len(sys.argv) == 3 and sys.argv[2] or setting.get_data_dir()
            __retrieve_data(data_dir)
        else:
            print("Usage: [index|retrieve] [data_dir]")
    else:
        print("Usage: [index|retrieve] [data_dir]")


if __name__ == "__main__":
    _main()
