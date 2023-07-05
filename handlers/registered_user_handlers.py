from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from services import quests_answers_sender
from data.database_filters import check_registered_sender_filter, check_reply_is_question_filter
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


@router.message(Command('id'))
async def process_get_id(message: Message):
    await message.answer(lexicon.ANSWERS['your_id'] + str(message.from_user.id))


@router.message(F.text == lexicon.BUTTONS['aks'])
async def process_ask(message: Message, state: FSMContext):
    await state.set_state(AskingStates.fill_id)
    await message.answer(lexicon.ANSWERS['write_id'], reply_markup=ReplyKeyboardRemove())


@router.message(F.text == lexicon.BUTTONS['my_questions'])
async def process_my_questions(message: Message, bot: Bot):
    await quests_answers_sender.resend_questions(bot, message.from_user.id)


@router.message(check_reply_is_question_filter)
async def handle_answering(message: Message, question: Question):
    await quests_answers_sender.send_answer(message, question)
    await message.answer(lexicon.ANSWERS['success_answer'])


@router.message()
async def handle_unknown_message(message: Message):
    await message.answer(lexicon.ANSWERS['unknown'])
