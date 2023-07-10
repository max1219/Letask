from aiogram import Bot
from data import database
from lexicon import lexicon
from services.question import Question
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError


async def send_question(bot: Bot, id_for: int, text: str, questioner_message: Message) -> bool:
    try:
        recipient_message = await bot.send_message(id_for, lexicon.ANSWERS['new_question'] + text)
    except TelegramForbiddenError:
        return False
    question = Question.from_messages(questioner_message, recipient_message)
    await database.add_question(question)
    return True


async def send_answer(bot: Bot, message: Message, question: Question) -> bool:
    try:
        await bot.send_message(
            chat_id=question.questioner_chat_id,
            text=lexicon.ANSWERS['new_answer'] + message.text,
            reply_to_message_id=question.questioner_message_id
        )
    except TelegramForbiddenError:
        return False
    await database.remove_question(question)
    return True


async def resend_questions(bot: Bot, user_id: int) -> None:
    questions: tuple[Question] = await database.get_user_questions(user_id)
    new_questions: list[Question] = list()
    if len(questions) == 0:
        await bot.send_message(user_id, lexicon.ANSWERS['not_have_questions'])
        return
    for question in questions:
        new_message = await bot.send_message(user_id, question.text)
        question.recipient_message_id = new_message.message_id
        new_questions.append(question)
    await database.update_questions(user_id, new_questions)
