"""Импорты класса Base и всех моделей для Alembic."""
from core.db import Base
from models.user import User
from models.task import Task, Period
from models.telegram import Telegram