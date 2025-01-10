import re
from llama_index.core.prompts import PromptTemplate
from llama_index.core.llms import LLM

from app.engine import models
from .prompts import next_question_prompt
from ..routes.payload import ChatMessages


def suggest_next_questions(
    chat_history: ChatMessages,
    response: str,
) -> list[str] | None:
    latest_user_message = None
    for message in reversed(chat_history.messages):
        if message.role == "user":
            latest_user_message = message
            break
    conversation: str = f"{latest_user_message}\n{response}"
    prompt_template = PromptTemplate(next_question_prompt)
    prompt = prompt_template.format(conversation=conversation)

    chat_model: LLM = models.get_chat_model()
    output = chat_model.complete(prompt)
    questions = _extract_questions(str(output))

    return questions


def _extract_questions(text: str) -> list[str] | None:
    content_match = re.search(r"```(.*?)```", text, re.DOTALL)
    content = content_match.group(1) if content_match else None
    if not content:
        return None
    return [q.strip() for q in content.split("\n") if q.strip()]
