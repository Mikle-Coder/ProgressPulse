from core.config import BOT_TOKEN, WEB_SERVER_HOST, WEB_SERVER_PORT, WEBHOOK_PATH, WEBHOOK_URL
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, enums, F
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application


async def on_startup(bot: Bot) -> None:
    from .utils.notify_admins import on_startup_notify
    from .utils.set_bot_commands import set_default_commands

    await on_startup_notify(bot)
    await set_default_commands(bot)
    logging.info("Bot has been started")
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")
    logging.info("Webhook has been set up")


async def on_shutdown(bot: Bot) -> None:
    logging.warning("Bot is being shut down...")
    await bot.delete_webhook()


async def run() -> None:
    from .handlers.users.start import rtr as start_rtr
    from .handlers.users.process import rtr as process_rtr
    from .handlers.users.total_duration import rtr as t_duration_rtr
    #from core.db import create_db
    #from .utils.task_timer import task_timer
    #from telegram_bot.handlers.users.process import task_timeout


    #task_timer.call_func = task_timeout
    #await create_db()

    dp = Dispatcher()
    dp.include_routers(start_rtr, process_rtr, t_duration_rtr)
    dp.message.filter(F.chat.type == "private")
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    bot = Bot(token=BOT_TOKEN, parse_mode=enums.ParseMode.MARKDOWN)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dp, bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    await web._run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)