async def on_startup(bot):
    from .utils.notify_admins import on_startup_notify
    from .utils.set_bot_commands import set_default_commands

    await on_startup_notify(bot)
    await set_default_commands(bot)

    print('Бот запущен')


async def run() -> None:
    from .handlers.users.start import rtr as start_rtr
    from .handlers.users.process import rtr as process_rtr
    from .handlers.users.total_duration import rtr as t_duration_rtr
    from aiogram import Bot, Dispatcher, enums, F
    from core.config import BOT_TOKEN
    from core.db import create_db
    import asyncio
    from .utils.task_timer import task_timer
    from telegram_bot.handlers.users.process import task_timeout

    task_timer.call_func = task_timeout

    #await create_db()
    bot = Bot(token=BOT_TOKEN, parse_mode=enums.ParseMode.MARKDOWN)
    dp = Dispatcher()


    dp.startup.register(on_startup)
    dp.include_routers(start_rtr, process_rtr, t_duration_rtr)
    dp.message.filter(F.chat.type == "private")
    await asyncio.gather(
        dp.start_polling(bot),
        task_timer.check_timeout()
    )
