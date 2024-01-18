from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Старт')
        ]
    ],
    resize_keyboard=True
)