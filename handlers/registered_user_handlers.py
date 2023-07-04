from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from data.database_filters import check_registered_filter
from lexicon import lexicon


router = Router()
router.message.filter(check_registered_filter)


@router.message(Command('start', 'help'))
async def process_start_help(message: Message):
    await message.answer(lexicon.ANSWERS['help'])


@router.message()
async def unknown(message: Message):
    await message.answer(lexicon.ANSWERS['unknown'])
