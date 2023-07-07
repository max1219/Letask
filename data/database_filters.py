from data import database
from aiogram.types import Message
from typing import Literal

from services.question import Question


def check_registered_sender_filter(message: Message) -> bool:
    return database.check_user_registered(message.from_user.id)


def check_registered_asked_filter(message: Message) -> bool:
    return message.text and message.text.isdigit() and database.check_user_registered(int(message.text))


def check_reply_is_question_filter(message: Message) -> dict[Literal['question'], Question] | None:
    if message.reply_to_message:
        for question in database.get_user_questions(message.from_user.id):
            if question.recipient_message_id == message.reply_to_message.message_id:
                return dict(question=question)
