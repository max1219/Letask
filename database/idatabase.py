from abc import ABC, abstractmethod
from collections.abc import Iterable

from services.question import Question


class IDatabase(ABC):
    # User(user_id PK, username)
    # Question(questioner_message_id PK, questioner_chat_id FK, recipient_message_id, recipient_chat_id FK, text)

    @abstractmethod
    async def check_id_registered(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def check_username_registered(self, username: str) -> bool:
        pass

    @abstractmethod
    async def add_user(self, user_id: int, username: str) -> None:
        pass

    @abstractmethod
    async def get_user_questions(self, user_id: int) -> Iterable[Question]:
        pass

    @abstractmethod
    async def add_question(self, question: Question) -> None:
        pass

    @abstractmethod
    async def remove_question(self, questioner_message_id: int) -> None:
        pass

    @abstractmethod
    async def update_recipient_message_id(self, question: Question) -> None:
        pass

    @abstractmethod
    async def update_many(self, questions: Iterable[Question]) -> None:
        pass
