import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    bot: TgBot


def load_config() -> Config:
    # Если на сервер можно выгрузить .env, то переменные окружения будут браться из него. Иначе их нужно указать
    # через какой нибудь встроенный в сервер способ задания переменных окружения
    if os.path.exists('.env'):
        load_dotenv()
    token = os.environ["BOT_TOKEN"]
    return Config(bot=TgBot(token))
