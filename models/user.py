from sqlalchemy import Column, Integer, DateTime, String, func
from core.db import Base


class Users(Base):
    telegram_user_id = Column(String(length=200))
    created_at = Column(DateTime(timezone=True), default=func.now())
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    username = Column(String(length=255))