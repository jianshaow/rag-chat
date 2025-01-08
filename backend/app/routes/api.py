from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from engine import chatter, models, config
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
    return VercelStreamingResponse(response)


@api.get("/{data}/files/{filename}", tags=["files"])
def download_file(data, filename):
    path = config.get_data_file(data, filename)
    return FileResponse(path=path)
