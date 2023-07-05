from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from lexicon import lexicon

menu_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text=lexicon.BUTTONS['aks']),
        KeyboardButton(text=lexicon.BUTTONS['my_questions'])
    ]],
    resize_keyboard=True
)

yes_no_inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text=lexicon.BUTTONS['yes'], callback_data='confirm_send'),
        InlineKeyboardButton(text=lexicon.BUTTONS['no'], callback_data='dont_confirm_send')
    ]]
)

close_inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text=lexicon.BUTTONS['close'], callback_data='close')
    ]]
)
