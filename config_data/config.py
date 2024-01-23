from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    bot: TgBot
