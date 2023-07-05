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


async def resend_questions(bot: Bot, user_id):
    user: UserRecord = database.get_user(user_id)
    questions: dict[int, Question] = user.questions
    new_questions: dict[int, Question] = dict()
    if len(questions) == 0:
        await bot.send_message(user_id, lexicon.ANSWERS['not_have_questions'])
        return
    for message_id, question in questions.items():
        text = question.recipient_message.text
        await question.recipient_message.delete()
        new_message = await bot.send_message(user_id, text)
        new_questions[new_message.message_id] = Question(questions[message_id].questioner_message, new_message)
    user.questions = new_questions
