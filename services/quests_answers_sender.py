from aiogram import Bot
from data import database
from data.user_record import UserRecord
from lexicon import lexicon
from services.question import Question
from aiogram.types import Message


async def send_question(bot: Bot, id_for: int, text: str, questioner_message: Message):
    recipient_message = await bot.send_message(id_for, lexicon.ANSWERS['new_question'] + text)
    user: UserRecord = database.get_user(id_for)
    user.questions[recipient_message.message_id] = Question(questioner_message, recipient_message)


async def send_answer(message: Message, question: Question):
    await question.questioner_message.reply(text=lexicon.ANSWERS['new_answer'] + message.text)
    user: UserRecord = database.get_user(message.from_user.id)
    del user.questions[message.reply_to_message.message_id]

