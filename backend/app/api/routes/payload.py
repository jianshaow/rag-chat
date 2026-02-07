import logging
from typing import (
    Annotated,
    Any,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    TypeVar,
    Union,
)

from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.schema import NodeWithScore
from mcp.types import CallToolResult, TextContent
from pydantic import BaseModel, Field

from app.api import files_base_url, tool_call_base_url

logger = logging.getLogger(__name__)


class SourceNode(BaseModel):
    id: str
    metadata: Dict[str, Any]
    score: Optional[float]
    text: str
    url: Optional[str]

    @classmethod
    def get_url_from_metadata(cls, metadata: Dict[str, Any]) -> Optional[str]:
        data_dir = metadata.get("data_dir")
        file_name = metadata.get("file_name")
        return f"{files_base_url}/{data_dir}/{file_name}"

    @classmethod
    def from_source_node(cls, source_node: NodeWithScore):
        metadata = source_node.node.metadata
        url = cls.get_url_from_metadata(metadata)

        return cls(
            id=source_node.node.node_id,
            metadata=metadata,
            score=source_node.score,
            text=source_node.node.text,  # type: ignore
            url=url,
        )

    @classmethod
    def from_source_nodes(cls, source_nodes: List[NodeWithScore]):
        return [cls.from_source_node(node) for node in source_nodes]

    @classmethod
    def from_call_tool_result(
        cls,
        result: CallToolResult,
        tool_id: str,
        tool_name: str,
        tool_kwargs: Dict[str, Any],
    ):
        return [
            cls(
                text=content.text,
                id=tool_id,
                metadata={
                    "source_type": "mcp",
                    "tool_name": tool_name,
                    "tool_kwargs": tool_kwargs,
                    "file_name": f"{tool_name}/mcp",
                },
                score=0,
                url=f"{tool_call_base_url}/{tool_name}",
            )
            for content in result.content
            if isinstance(content, TextContent)
        ]


class TextPart(BaseModel):
    type: Literal["text"]
    text: str


class FileData(BaseModel):
    filename: str
    media_type: str = Field(alias="mediaType")
    url: str
    model_config = {"populate_by_name": True}


class SourceData(BaseModel):
    nodes: List[SourceNode]


T = TypeVar("T")


class DataPart(BaseModel, Generic[T]):
    id: str | None = None
    type: str
    data: T


class FilePart(DataPart[FileData]):
    type: Literal["data-file"]


class SourcesPart(DataPart[SourceData]):
    type: Literal["data-sources"]


MessagePart = Annotated[
    Union[
        TextPart,
        FilePart,
        SourcesPart,
    ],
    Field(discriminator="type"),
]


class Message(BaseModel):
    id: str
    role: MessageRole
    parts: List[MessagePart] = []

    @property
    def content(self) -> str:
        if self.parts is None:
            return ""
        content_parts = []
        for part in self.parts:
            if isinstance(part, TextPart):
                content_parts.append(part.text)
                continue
        return "\n".join(content_parts)


class ChatMessages(BaseModel):
    id: str
    trigger: str | None = None
    messages: List[Message]

    @property
    def last_content(self) -> str:
        last_message = self.messages[-1]
        message_content = last_message.content
        return message_content

    @property
    def history(self) -> list[ChatMessage]:
        chat_messages = [
            ChatMessage(role=message.role, content=message.content)
            for message in self.messages[:-1]
        ]
        return chat_messages

    @property
    def chat_messages(self) -> list[ChatMessage]:
        chat_messages = [
            ChatMessage(role=message.role, content=message.content)
            for message in self.messages
        ]
        return chat_messages

    def get_document_files(self) -> List[FileData]:
        doc_files: List[FileData] = []
        for message in self.messages:
            if message.role == MessageRole.USER and message.parts is not None:
                for part in message.parts:
                    if isinstance(part, FilePart):
                        doc_files.append(part.data)
        return doc_files

    def __str__(self) -> str:
        return str(
            [
                {"role": message.role, "content": message.content}
                for message in self.messages
            ]
        )

    def __repr__(self) -> str:
        return str(self.messages)


class DocumentFile(BaseModel):
    id: str
    name: str
    type: str
    size: int
    url: str
    path: Optional[str] = Field(
        None,
        exclude=True,
    )
    refs: Optional[List[str]] = Field(None)


class FileUploadRequest(BaseModel):
    base64: str
    name: str
    params: Any = None


class QueryResult(BaseModel):
    answer: str
    sources: List[SourceNode]
