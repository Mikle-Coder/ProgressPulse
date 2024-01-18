from telegram_bot import app as bot

if __name__ == "__main__":
    import logging, sys, asyncio
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(bot.run())