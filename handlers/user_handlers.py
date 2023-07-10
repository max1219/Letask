from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter

from keyboards.keyboards import menu_kb
from services import quests_answers_sender
from data import database_processor
from lexicon import lexicon
from services.question import Question
from states.states import AskingStates
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

router: Router = Router()
router.message.filter(StateFilter(default_state))


@router.message(Command('start', 'help'))
async def process_start_help(message: Message) -> None:
    await message.answer(lexicon.ANSWERS['help'], reply_markup=menu_kb)


@router.message(F.text == lexicon.BUTTONS['aks'])
async def process_ask(message: Message, state: FSMContext) -> None:
    await state.set_state(AskingStates.fill_username)
    await message.answer(lexicon.ANSWERS['write_recipient'], reply_markup=ReplyKeyboardRemove())


@router.message(F.text == lexicon.BUTTONS['my_questions'])
async def process_my_questions(message: Message, bot: Bot) -> None:
    await quests_answers_sender.resend_questions(bot, message.from_user.id)


@router.message(F.reply_to_message)
async def handle_answering(message: Message, bot: Bot) -> None:
    question: Question = await database_processor.get_question_from_reply(message.chat.id, message.reply_to_message)
    if question:
        await quests_answers_sender.send_answer(bot, message, question)
        await message.answer(lexicon.ANSWERS['success_answer'])
    else:
        await message.answer(lexicon.ANSWERS['is_not_question'])


@router.message()
async def handle_unknown_message(message: Message) -> None:
    await message.answer(lexicon.ANSWERS['unknown'])
