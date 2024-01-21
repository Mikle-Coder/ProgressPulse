from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .names import PAUSE, STOP, RESUME

kb_process_on = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=PAUSE),
            KeyboardButton(text=STOP)
        ]
    ],
    resize_keyboard=False
)

kb_process_off = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=RESUME),
            KeyboardButton(text=STOP)
        ]
    ],
    resize_keyboard=False
)