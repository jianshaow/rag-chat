from fastapi import APIRouter, Request

from app.engine import models, events, engines
from .vercel import VercelStreamingResponse

chat_router = r = APIRouter()


@r.get("/config", tags=["chat"])
def chat_config():
    return {"starterQuestions": None}


@r.post("", tags=["chat"])
async def chat(request: Request):
    messages = (await request.json())["messages"]
    chat_messages = models.ChatMessages(messages)
    engine = engines.get_chat_engine("en_novel")
    response = engine.astream_chat(chat_messages.last, chat_messages.history)
    return VercelStreamingResponse(events.event_handler, messages, response)
