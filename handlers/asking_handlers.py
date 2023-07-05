from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from data.database_filters import check_registered_asked_filter
from lexicon import lexicon
from states.states import AskingStates
from aiogram.fsm.context import FSMContext
from keyboards import keyboards
from services import quests_answers_sender
from keyboards.keyboards import menu_kb


router = Router()
router.message.filter(StateFilter(*AskingStates.get_states()))


@router.message(StateFilter(AskingStates.fill_id), check_registered_asked_filter)
async def fill_id(message: Message, state: FSMContext):
    await state.set_state(AskingStates.fill_text)
    await state.update_data(id=message.text)
    await message.answer(lexicon.ANSWERS['write_text'])


@router.message(StateFilter(AskingStates.fill_id))
async def wrong_id(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(lexicon.ANSWERS['wrong_id'], reply_markup=menu_kb)


@router.message(StateFilter(AskingStates.fill_text))
async def fill_text(message: Message, state: FSMContext):
    await state.set_state(AskingStates.confirming)
    await state.update_data(text=message.text)
    id_text_dict = await state.get_data()
    question_text, user_id = id_text_dict['text'], id_text_dict['id']
    answer_text = user_id + '\n' + question_text + '\n' + lexicon.ANSWERS['check_again']
    await message.answer(answer_text, reply_markup=keyboards.yes_no_inline_kb)


@router.message()
async def wrong_answer(message: Message):
    await message.answer(lexicon.ANSWERS['unknown'])


@router.callback_query(StateFilter(AskingStates.confirming))
async def confirm(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if callback.data == 'confirm_send':
        id_text_dict = await state.get_data()
        await quests_answers_sender.send_question(bot, int(id_text_dict['id']), id_text_dict['text'], callback.message)
        await callback.message.answer(lexicon.ANSWERS['success_question'], reply_markup=menu_kb)
    await callback.message.delete_reply_markup()
    await state.clear()
