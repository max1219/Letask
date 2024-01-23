from abc import ABC, abstractmethod

from config_data import Config


class IConfigLoader(ABC):
    @abstractmethod
    def load_config(self) -> Config:
        pass
