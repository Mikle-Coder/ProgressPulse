from telegram_bot import app as bot

if __name__ == "__main__":
    import logging
    import sys
    import asyncio
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(bot.run())
