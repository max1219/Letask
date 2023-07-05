from dataclasses import dataclass, field
from aiogram.types import Message


@dataclass
class Question:
    questioner_message: Message = field(hash=False)
    recipient_message: Message = field(hash=False)

    def __hash__(self):
        return hash((self.questioner_message.from_user.id, self.recipient_message.from_user.id))
