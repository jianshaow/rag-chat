import logging
from fastapi import APIRouter, Request, HTTPException

from app.engine import events, engines
from app.api.services.files import DocumentFile, process_file
from .vercel import VercelStreamingResponse
from .payload import FileUploadRequest, ChatMessages

logger = logging.getLogger(__name__)

chat_router = r = APIRouter()


@r.get("/config", tags=["chat"])
def chat_config():
    return {"starterQuestions": None}


@r.post("", tags=["chat"])
async def chat(request: Request, chat_messages: ChatMessages):
    """
    Chat with agent based on data.
    """
    engine = engines.get_chat_engine("en_novel")
    response = engine.astream_chat(chat_messages.last_content, chat_messages.history)
    return VercelStreamingResponse(events.event_handler, chat_messages, response)


@r.post("/upload", tags=["chat"])
def upload_file(request: FileUploadRequest) -> DocumentFile:
    """
    To upload a file from frontend.
    """
    try:
        return process_file(request.name, request.base64, request.params)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing file")
