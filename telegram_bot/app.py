async def on_startup(bot):
    from utils.notify_admins import on_startup_notify
    from utils.set_bot_commands import set_default_commands

    await on_startup_notify(bot)
    await set_default_commands(bot)

    print('Бот запущен')


async def main() -> None:
    from loader import bot
    from handlers import dp
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import logging, sys, asyncio
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())