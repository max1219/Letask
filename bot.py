import asyncio
from config_data.config import Config, load_config
from aiogram import Bot, Dispatcher
from handlers import user_handlers, asking_handlers
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares.registered_checker_middleware import RegisteredCheckerMiddleware


async def main() -> None:
    config: Config = load_config()
    storage: MemoryStorage = MemoryStorage()

    bot: Bot = Bot(config.bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.update.outer_middleware(RegisteredCheckerMiddleware())

    dp.include_router(asking_handlers.router)
    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
