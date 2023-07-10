import os
from dataclasses import dataclass
from typing import Iterable

from dotenv import load_dotenv


@dataclass
class TgBot:
    token: str
    admin_ids: Iterable[int]


@dataclass
class Config:
    bot: TgBot


def load_config() -> Config:
    # Если на сервер можно выгрузить .env, то переменные окружения будут браться из него. Иначе их нужно указать
    # через какой нибудь встроенный в сервер способ задания переменных окружения
    if os.path.exists('.env'):
        load_dotenv()
    token = os.environ["BOT_TOKEN"]
    admin_ids = os.environ["ADMIN_IDS"]
    admin_ids = tuple(map(int, admin_ids.split(',')))
    return Config(bot=TgBot(token=token, admin_ids=admin_ids))
