import os
from typing import Any, Dict, List, Optional

from llama_index.core.llms import ChatMessage, MessageRole
from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

from app.api.services.files import DocumentFile


class AnnotationFileData(BaseModel):
    files: List[DocumentFile] = Field(
        default=[],
        description="List of files",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "files": [
                    {
                        "content": "data:text/plain;base64,aGVsbG8gd29ybGQK=",
                        "name": "example.txt",
                    }
                ]
            }
        }
        alias_generator = to_camel

    @staticmethod
    def _get_url_llm_content(file: DocumentFile) -> Optional[str]:
        url_prefix = os.getenv("FILESERVER_URL_PREFIX")
        if url_prefix:
            if file.url is not None:
                return f"File URL: {file.url}\n"
            else:
                return f"File URL (instruction: do not update this file URL yourself): {url_prefix}/output/uploaded/{file.name}\n"
        else:
            print(
                "Warning: FILESERVER_URL_PREFIX not set in environment variables. Can't use file server"
            )
            return None

    @classmethod
    def _get_file_content(cls, file: DocumentFile) -> str:
        """
        Construct content for LLM from the file metadata
        """
        default_content = f"=====File: {file.name}=====\n"
        # Include file URL if it's available
        url_content = cls._get_url_llm_content(file)
        if url_content:
            default_content += url_content
        # Include document IDs if it's available
        if file.refs is not None:
            default_content += f"Document IDs: {file.refs}\n"
        # file path
        sandbox_file_path = f"/tmp/{file.name}"
        local_file_path = f"output/uploaded/{file.name}"
        default_content += f"Sandbox file path (instruction: only use sandbox path for artifact or code interpreter tool): {sandbox_file_path}\n"
        default_content += f"Local file path (instruction: Use for local tools: form filling, extractor): {local_file_path}\n"
        return default_content

    def to_llm_content(self) -> Optional[str]:
        file_contents = [self._get_file_content(file) for file in self.files]
        if len(file_contents) == 0:
            return None
        return "Use data from following files content\n" + "\n".join(file_contents)


class AgentAnnotation(BaseModel):
    agent: str
    text: str


class ArtifactAnnotation(BaseModel):
    toolCall: Dict[str, Any]
    toolOutput: Dict[str, Any]


class Annotation(BaseModel):
    type: str
    data: AnnotationFileData | List[str] | AgentAnnotation | ArtifactAnnotation

    def to_content(self) -> Optional[str]:
        if self.type == "document_file" and isinstance(self.data, AnnotationFileData):
            return self.data.to_llm_content()
        elif self.type == "image":
            raise NotImplementedError("Use image file is not supported yet!")
        else:
            print(
                f"The annotation {self.type} is not supported for generating context content"
            )
        return None


class Message(BaseModel):
    role: MessageRole
    content: str
    annotations: List[Annotation] | None = None


class ChatMessages(BaseModel):
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

    def get_chat_document_ids(self) -> List[str]:
        document_ids: List[str] = []
        uploaded_files = self.get_document_files()
        for _file in uploaded_files:
            refs = getattr(_file, "refs", None)
            if refs is not None:
                document_ids.extend(refs)
        return list(set(document_ids))

    def get_document_files(self) -> List[DocumentFile]:
        uploaded_files = []
        for message in self.messages:
            if message.role == MessageRole.USER and message.annotations is not None:
                for annotation in message.annotations:
                    if annotation.type == "document_file" and isinstance(
                        annotation.data, AnnotationFileData
                    ):
                        uploaded_files.extend(annotation.data.files)
        return uploaded_files

    def __str__(self) -> str:
        return str(
            [
                {"role": message.role, "content": message.content}
                for message in self.messages
            ]
        )

    def __repr__(self) -> str:
        return str(self.messages)


class FileUploadRequest(BaseModel):
    base64: str
    name: str
    params: Any = None
