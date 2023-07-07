from aiogram.types import Message


class Question:
    __slots__ = 'text', 'questioner_message_id', 'questioner_chat_id', 'recipient_message_id', 'recipient_chat_id'

    def __init__(self, questioner_message: Message, recipient_message: Message) -> None:
        self.text = recipient_message.text
        self.questioner_message_id = questioner_message.message_id
        self.questioner_chat_id = questioner_message.chat.id
        self.recipient_message_id = recipient_message.message_id
        self.recipient_chat_id = recipient_message.chat.id
