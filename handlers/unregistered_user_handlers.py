from aiogram import Router
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter
from data import database
from lexicon import lexicon
from data.database_filters import check_registered_sender_filter
from keyboards.keyboards import menu_kb


router: Router = Router()
router.message.filter(lambda message: not check_registered_sender_filter(message), StateFilter(default_state))


@router.message(CommandStart())
async def process_start(message: Message):
    database.add_user(message.from_user.id)
    await message.answer(lexicon.ANSWERS['greet'] + str(message.from_user.id), reply_markup=menu_kb)


@router.message()
async def other(message: Message):
    await message.answer(lexicon.ANSWERS['not_registered'])
