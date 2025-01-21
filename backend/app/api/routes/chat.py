import logging

from fastapi import APIRouter, HTTPException

from app.api.routes.filters import generate_filters
from app.api.routes.payload import ChatMessages, FileUploadRequest
from app.api.routes.vercel import VercelStreamingResponse
from app.api.services.files import DocumentFile, process_file
from app.engine import engines

logger = logging.getLogger(__name__)

chat_router = r = APIRouter()


@r.get("/config", tags=["chat"])
def chat_config():
    return {"starterQuestions": None}


@r.post("", tags=["chat"])
async def chat(chat_messages: ChatMessages):
    """
    Chat with agent based on data.
    """
    doc_ids = chat_messages.get_chat_document_ids()
    data, filters = generate_filters(doc_ids)
    engine, handler = engines.get_chat_engine(data, filters)
    response = engine.astream_chat(chat_messages.last_content, chat_messages.history)
    return VercelStreamingResponse(handler, chat_messages, response)


@r.post("/upload", tags=["chat"])
def upload_file(request: FileUploadRequest) -> DocumentFile:
    """
    To upload a file from frontend.
    """
    try:
        return process_file(request.name, request.base64, request.params)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing file") from e
