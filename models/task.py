from sqlalchemy import Column, Integer, DateTime, String, func, ForeignKey
from core.db import Base, CRUD
from sqlalchemy.orm import relationship


class Result(Base, CRUD):
    task_id = Column(Integer, ForeignKey('task.id'))
    text = Column(String)


class Period(Base, CRUD):
    task_id = Column(Integer, ForeignKey('task.id'))
    started_at = Column(DateTime(timezone=True), default=func.now())
    ended_at = Column(DateTime(timezone=True))


class Task(Base, CRUD):
    user_id = Column(Integer, ForeignKey('user.id'))
    description = Column(String)
    result = relationship(Result, uselist=False, cascade="all, delete")
    periods = relationship(Period, cascade="all, delete")