import asyncio
from config_data.config import Config, load_config
from aiogram import Bot, Dispatcher
from handlers import registered_user_handlers, unregistered_user_handlers


async def main():
    config: Config = load_config()

    bot: Bot = Bot(config.bot.token)
    dp: Dispatcher = Dispatcher()

    dp.include_router(registered_user_handlers.router)
    dp.include_router(unregistered_user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())