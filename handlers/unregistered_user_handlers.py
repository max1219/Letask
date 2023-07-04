from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from data import database
from lexicon import lexicon
from data.database_filters import check_registered_filter


router: Router = Router()
router.message.filter(lambda message: not check_registered_filter(message))


@router.message(CommandStart())
async def process_start(message: Message):
    database.add_user(message.from_user.id)
    await message.answer(lexicon.ANSWERS['help'])


@router.message()
async def other(message: Message):
    await message.answer(lexicon.ANSWERS['not_registered'])