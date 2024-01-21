from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import relationship
from core.db import Base, CRUD
from models.telegram import Telegram
from models.task import Task


class User(Base, CRUD):
    created_at = Column(DateTime(timezone=True), default=func.now())
    telegram = relationship(Telegram, uselist=False, backref='user', cascade="all, delete")
    tasks = relationship(Task, backref='user', cascade="all, delete")
