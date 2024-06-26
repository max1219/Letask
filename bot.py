import asyncio
import logging
import sys

from config_data import Config, DotenvConfigLoader
from aiogram import Bot, Dispatcher
from database import IDatabase, Sqlite3Database
from handlers import user_handlers, asking_handlers
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares.registered_checker_middleware import RegisteredCheckerMiddleware


async def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format='[{asctime}] #{levelname:8} {filename}:'
               '{lineno} - {message}',
        style='{',
        handlers=(logging.StreamHandler(stream=sys.stdout),
                  logging.FileHandler("logs/log.txt"),
                  logging.FileHandler("logs/last_log.txt", mode="w"))
    )
    logging.info("Start of initialization")

    config: Config = DotenvConfigLoader().load_config()
    # todo заменить на другое хранилище
    storage: MemoryStorage = MemoryStorage()

    bot: Bot = Bot(config.bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)

    database: IDatabase = Sqlite3Database()
    dp["database"] = database

    dp.update.outer_middleware(RegisteredCheckerMiddleware())

    dp.include_router(asking_handlers.router)
    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    logging.info("Bot started")

if __name__ == '__main__':
    asyncio.run(main())
