async def on_startup(bot):
    from .utils.notify_admins import on_startup_notify
    from .utils.set_bot_commands import set_default_commands

    await on_startup_notify(bot)
    await set_default_commands(bot)

    print('Бот запущен')


async def run() -> None:
    from .handlers.users.start import rtr as start_rtr
    from .handlers.users.process import rtr as process_rtr
    from aiogram import Bot, Dispatcher, enums, filters, F
    from core.config import BOT_TOKEN

    bot = Bot(token=BOT_TOKEN, parse_mode=enums.ParseMode.HTML)
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.include_routers(start_rtr, process_rtr)
    dp.message.filter(F.chat.type == "private")
    await dp.start_polling(bot)
