from fastapi import APIRouter, Request

from app.engine import chatter, models, events
from .vercel import VercelStreamingResponse

chat_router = r = APIRouter()


@r.get("/config", tags=["chat"])
def chat_config():
    return {"starterQuestions": None}


@r.post("", tags=["chat"])
async def chat(request: Request):
    messages = (await request.json())["messages"]
    chat_messages = models.ChatMessages(messages)
    response = chatter.chat("en_novel", chat_messages)
    return VercelStreamingResponse(events.event_callback_handler, messages, response)
