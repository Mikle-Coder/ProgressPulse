from aiogram.types import BotCommand as bc
from aiogram import Bot


async def set_default_commands(bot: Bot):
    await bot.set_my_commands([
        bc(command='start', description='Запустить бота'),
        bc(command='help', description='Помощь'),
    ])