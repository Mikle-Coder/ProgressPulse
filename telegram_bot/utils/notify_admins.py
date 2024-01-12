import logging
from aiogram import Bot
from data.config import ADMIN_ID


async def on_startup_notify(bot: Bot):
    try:
        text = 'Бот запущен'
        await bot.send_message(chat_id=ADMIN_ID, text=text)
    except Exception as err:
        logging.exception(err)