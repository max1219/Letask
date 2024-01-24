from dataclasses import dataclass

from aiogram.types import Message


@dataclass(slots=True)
class Question:
    questioner_message_id: int
    questioner_chat_id: int
    recipient_message_id: int
    recipient_chat_id: int
    text: str

    @classmethod
    def from_messages(cls, questioner_message: Message, recipient_message: Message) -> "Question":
        return cls(questioner_message.message_id, questioner_message.chat.id,
                   recipient_message.message_id, recipient_message.chat.id, recipient_message.text)
