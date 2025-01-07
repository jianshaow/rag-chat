from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from engine import chatter, models, config
from app.routes.vercel import stream_gen

api = APIRouter()


@api.get("/chat/config", tags=["chat"])
def chat_config():
    return {"starterQuestions": None}


@api.post("/chat", tags=["chat"])
async def chat(request: Request):
    messages = (await request.json())["messages"]
    chat_messages = models.ChatMessages(messages)
    response = chatter.chat("en_novel", chat_messages)
    return stream_gen(response)


@api.get("/<data>/files/<filename>", tags=["files"])
def download_file(data, filename):
    data_dir = config.get_data_path(data)
    return FileResponse(path=data_dir, filename=filename)
