from data import database
from aiogram.types import Message

from services.question import Question


async def get_question_from_reply(recipient_id: int, message: Message) -> Question | None:
    for question in await database.get_user_questions(recipient_id):
        if question.recipient_message_id == message.message_id:
            return question
