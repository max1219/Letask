from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from services import quests_answers_sender
from data import database
from data.database_filters import check_registered_sender_filter, check_answer_filter
from lexicon import lexicon
from services.question import Question
from states.states import AskingStates
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


router = Router()
router.message.filter(check_registered_sender_filter, StateFilter(default_state))


@router.message(Command('start', 'help'))
async def process_start_help(message: Message):
    await message.answer(lexicon.ANSWERS['help'])


@router.message(F.text == lexicon.BUTTONS['aks'])
async def process_ask(message: Message, state: FSMContext):
    await state.set_state(AskingStates.fill_id)
    await message.answer(lexicon.ANSWERS['write_id'], reply_markup=ReplyKeyboardRemove())


@router.message(check_answer_filter)
async def handle_answering(message: Message, question: Question):
    await quests_answers_sender.send_answer(message, question)
    await message.answer(lexicon.ANSWERS['success_answer'])


@router.message()
async def handle_unknown_message(message: Message):

    await message.answer(lexicon.ANSWERS['unknown'])
