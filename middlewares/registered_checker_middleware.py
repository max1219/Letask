from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from data import database
from keyboards.keyboards import menu_kb
from lexicon import lexicon


class RegisteredCheckerMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user_id: int = data['event_from_user'].id
        username: str = data['event_from_user'].username
        if not await database.check_user_id_registered(user_id):
            bot: Bot = data['bot']
            await database.add_user(user_id, username)
            await bot.send_message(user_id, lexicon.ANSWERS['greet'], reply_markup=menu_kb)
        return await handler(event, data)
