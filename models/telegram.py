from sqlalchemy import Column, String, Integer, ForeignKey
from core.db import Base, CRUD


class Telegram(Base, CRUD):
    telegram_id = Column(Integer, unique=True)
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    username = Column(String(length=255))
    user_id = Column(Integer, ForeignKey('user.id'))