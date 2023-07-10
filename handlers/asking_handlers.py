from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from lexicon import lexicon
from states.states import AskingStates
from aiogram.fsm.context import FSMContext
from keyboards import keyboards
from services import quests_answers_sender
from keyboards.keyboards import menu_kb
from data import database

router: Router = Router()
router.message.filter(StateFilter(*AskingStates.get_states()))


@router.message(StateFilter(AskingStates.fill_username), F.text.startswith('@'))
async def fill_username(message: Message, state: FSMContext) -> None:
    username: str = message.text.lower()
    if username[1:] == message.from_user.username:
        await message.answer_photo(photo=lexicon.PHOTOS['dont_ask_yourself'],
                                   caption=lexicon.ANSWERS['dont_ask_yourself'],
                                   reply_markup=menu_kb)
        await state.clear()
        return
    if await database.check_username_registered(username[1:]):
        await state.set_state(AskingStates.fill_text)
        await state.update_data(username=username)
        await message.answer(lexicon.ANSWERS['write_text'])
    else:
        await state.clear()
        await message.answer(lexicon.ANSWERS['user_not_found'], reply_markup=menu_kb)


@router.message(StateFilter(AskingStates.fill_username))
async def wrong_username_format(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(lexicon.ANSWERS['wrong_username_format'], reply_markup=menu_kb)


@router.message(StateFilter(AskingStates.fill_text))
async def fill_text(message: Message, state: FSMContext) -> None:
    await state.set_state(AskingStates.confirming)
    await state.update_data(text=message.text)
    username_text_dict: dict = await state.get_data()
    question_text = username_text_dict['text']
    username = username_text_dict['username']
    answer_text = username + '\n' + question_text + '\n' + lexicon.ANSWERS['check_again']
    await message.answer(answer_text, reply_markup=keyboards.yes_no_inline_kb)


@router.message()
async def wrong_answer(message: Message) -> None:
    await message.answer(lexicon.ANSWERS['unknown'])


@router.callback_query(StateFilter(AskingStates.confirming))
async def confirm(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    if callback.data == 'confirm_send':
        username_text_dict: dict = await state.get_data()
        question_text = username_text_dict['text']
        username = username_text_dict['username']
        user_id = await database.get_user_id(username[1:])
        is_success = await quests_answers_sender.send_question(bot, user_id, question_text,
                                                               callback.message)
        await callback.message.answer(lexicon.ANSWERS['success_question' if is_success else 'cant_ask'],
                                      reply_markup=menu_kb)
    await callback.message.delete_reply_markup()
    await state.clear()
