from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from keyboards.keyboards import menu_kb
from lexicon import lexicon
from database import IDatabase


class RegisteredCheckerMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user_id: int = data['event_from_user'].id
        db: IDatabase = data["database"]
        if not await db.check_id_registered(user_id):
            username: str = data['event_from_user'].username
            bot: Bot = data['bot']
            if not username:
                await bot.send_message(user_id, lexicon.ANSWERS['you_dont_have_username'])
                return
            await db.add_user(user_id, username.lower())
            await bot.send_message(user_id, lexicon.ANSWERS['greet'], reply_markup=menu_kb)
        else:
            return await handler(event, data)
