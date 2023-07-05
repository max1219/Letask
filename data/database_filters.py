from data import database
from aiogram.types import Message
from typing import Literal

from services.question import Question


def check_registered_sender_filter(message: Message) -> bool:
    return database.get_user(message.from_user.id) is not None


def check_registered_asked_filter(message: Message) -> bool:
    return message.text and message.text.isdigit() and database.get_user(int(message.text)) is not None


def check_reply_is_question_filter(message: Message) -> dict[Literal['question'], Question] | None:
    if message.reply_to_message and message.reply_to_message.message_id in \
            database.get_user(message.from_user.id).questions:
        return dict(question=database.get_user(message.from_user.id).questions[message.reply_to_message.message_id])
