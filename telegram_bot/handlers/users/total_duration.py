from aiogram import types, filters, Router
from models.user import User
from core.db import Session
from datetime import timedelta
from aiogram.utils.markdown import bold


rtr = Router()


@rtr.message(filters.Command('total_duration'))
async def cmd_total_duration(message: types.Message):
    chat = message.chat
    async with Session() as session:
        user = await User.get_by_telegram_id(session, chat.id)
        if user:
            seconds = await user.get_total_duration(session)
            duration = timedelta(seconds=seconds)
            text = '⏳ Твое общее время: ' + bold(duration)
    await message.answer(text=text, reply_markup=message.reply_markup)