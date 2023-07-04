from data import database
from aiogram.types import Message


def check_registered_filter(message: Message) -> bool:
    return database.get_user(message.from_user.id) is not None
