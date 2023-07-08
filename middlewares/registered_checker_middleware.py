from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from data import database
from lexicon import lexicon


class RegisteredCheckerMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user_id: int = data['event_from_user'].id
        if not database.check_user_registered(user_id):
            database.add_user(user_id)
        return await handler(event, data)
