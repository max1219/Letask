from collections.abc import Iterator
from itertools import chain

from aiogram import Bot
from database import IDatabase
from lexicon import lexicon
from services.question import Question
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError


async def send_question(bot: Bot, user_id: int, text: str, questioner_message: Message, database: IDatabase) -> bool:
    try:
        recipient_message = await bot.send_message(user_id, lexicon.ANSWERS['new_question'] + text)
    except TelegramForbiddenError:
        return False
    question = Question.from_messages(questioner_message, recipient_message)
    await database.add_question(question)
    return True


async def send_answer(bot: Bot, message: Message, question: Question, database: IDatabase) -> bool:
    try:
        await bot.send_message(
            chat_id=question.questioner_chat_id,
            text=lexicon.ANSWERS['new_answer'] + message.text,
            reply_to_message_id=question.questioner_message_id
        )
    except TelegramForbiddenError:
        return False
    await database.remove_question(question.questioner_message_id)
    return True


async def resend_questions(bot: Bot, user_id: int, database: IDatabase) -> None:
    questions_iterator: Iterator[Question] = iter(await database.get_user_questions(user_id))
    new_questions: list[Question] = list()

    first = next(questions_iterator, None)
    if first is None:
        await bot.send_message(user_id, lexicon.ANSWERS['not_have_questions'])
        return

    questions_iterator = chain([first], questions_iterator)

    for question in questions_iterator:
        new_message = await bot.send_message(user_id, question.text)
        question.recipient_message_id = new_message.message_id
        new_questions.append(question)
    await database.update_many(new_questions)
