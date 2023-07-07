from aiogram import Bot
from data import database
from lexicon import lexicon
from services.question import Question
from aiogram.types import Message


async def send_question(bot: Bot, id_for: int, text: str, questioner_message: Message) -> None:
    recipient_message = await bot.send_message(id_for, lexicon.ANSWERS['new_question'] + text)
    question = Question(questioner_message, recipient_message)
    database.add_question(question)


async def send_answer(bot: Bot, message: Message, question: Question) -> None:
    await bot.send_message(
        chat_id=question.questioner_chat_id,
        text=lexicon.ANSWERS['new_answer'] + message.text,
        reply_to_message_id=question.questioner_message_id
    )
    database.remove_question(question)


async def resend_questions(bot: Bot, user_id: int) -> None:
    questions: list[Question] = database.get_user_questions(user_id)
    if len(questions) == 0:
        await bot.send_message(user_id, lexicon.ANSWERS['not_have_questions'])
        return
    for question in questions:
        new_message = await bot.send_message(user_id, question.text)
        question.recipient_message_id = new_message.message_id

    database.update_user_questions(user_id, questions)
