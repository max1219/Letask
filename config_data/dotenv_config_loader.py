import logging
import os
import dotenv

from config_data import IConfigLoader, Config, TgBot


class DotenvConfigLoader(IConfigLoader):
    def __init__(self, env_name: str = ".env"):
        self._env_name = env_name

    def load_config(self) -> Config:
        if not os.path.exists(self._env_name):
            logging.critical(f"Env {self._env_name} not found")

        dotenv.load_dotenv(dotenv_path=self._env_name)
        token = os.environ["BOT_TOKEN"]
        logging.debug(f"Token: {token}")
        logging.info("Config has been loaded")
        return Config(bot=TgBot(token=token))
