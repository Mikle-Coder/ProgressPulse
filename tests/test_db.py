import sys
from pathlib import Path

# Получаем путь к текущему файлу
current_dir = Path(__file__).resolve().parent

# Добавляем директорию с модулями в sys.path
sys.path.append(str(current_dir.parent))


from models.telegram import Telegram
from models.user import User
from core.db import AsyncSessionLocal
import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def create_db_test():
    async with AsyncSessionLocal as session:
        user = await User.create(session)
        telegram = await Telegram.create(session, telegram_id=1111)