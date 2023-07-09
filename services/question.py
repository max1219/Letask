from aiogram.types import Message


class Question:
    __slots__ = 'text', 'questioner_message_id', 'questioner_chat_id', 'recipient_message_id', 'recipient_chat_id'

    def __init__(self, text, questioner_message_id, questioner_chat_id, recipient_message_id, recipient_chat_id):
        self.text = text
        self.questioner_message_id = questioner_message_id
        self.questioner_chat_id = questioner_chat_id
        self.recipient_message_id = recipient_message_id
        self.recipient_chat_id = recipient_chat_id

    @classmethod
    def from_messages(cls, questioner_message: Message, recipient_message: Message) -> "Question":
        return cls(recipient_message.text, questioner_message.message_id, questioner_message.chat.id,
                   recipient_message.message_id, recipient_message.chat.id)
