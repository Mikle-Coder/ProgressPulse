from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .names import START


kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=START)
        ]
    ],
    resize_keyboard=False
)