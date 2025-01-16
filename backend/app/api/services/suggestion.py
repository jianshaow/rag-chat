import re
from typing import List
from llama_index.core.prompts import PromptTemplate
from llama_index.core.llms import LLM, ChatMessage, MessageRole

from app.engine import models
from app.api.services.prompts import next_question_prompt


async def suggest_next_questions(
    chat_history: List[ChatMessage], response: str
) -> list[str] | None:
    latest_user_message = None
    for message in reversed(chat_history):
        if message.role == MessageRole.USER:
            latest_user_message = message
            break
    conversation: str = f"{latest_user_message}\n{response}"
    prompt_template = PromptTemplate(next_question_prompt)
    prompt = prompt_template.format(conversation=conversation)

    chat_model = models.get_chat_model()
    output = await chat_model.acomplete(prompt)
    questions = _extract_questions(output.text)

    return questions


def _extract_questions(text: str) -> list[str] | None:
    content_match = re.search(r"```(.*?)```", text, re.DOTALL)
    content = content_match.group(1) if content_match else None
    if not content:
        return None
    return [q.strip() for q in content.split("\n") if q.strip()]
