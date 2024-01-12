from data import config
from aiogram import Bot, Dispatcher, enums


bot = Bot(token=config.BOT_TOKEN, parse_mode=enums.ParseMode.HTML)
dp = Dispatcher()