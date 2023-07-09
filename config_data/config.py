import os
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    bot: TgBot


def load_config(path: str | None = None) -> Config:
    token = os.environ["BOT_TOKEN"]
    return Config(bot=TgBot(token))
