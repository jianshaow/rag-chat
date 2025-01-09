from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from app.engine import chatter, models, config, events
from .vercel import VercelStreamingResponse

api = APIRouter()


@api.get("/chat/config", tags=["chat"])
def chat_config():
    return {"starterQuestions": None}


@api.post("/chat", tags=["chat"])
async def chat(request: Request):
    messages = (await request.json())["messages"]
    chat_messages = models.ChatMessages(messages)
    response = chatter.chat("en_novel", chat_messages)
    return VercelStreamingResponse(events.event_callback_handler, messages, response)


@api.get("/{data}/files/{filename}", tags=["files"])
def download_file(data, filename):
    path = config.get_data_file(data, filename)
    return FileResponse(path=path)
