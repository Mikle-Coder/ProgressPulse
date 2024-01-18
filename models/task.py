from sqlalchemy import Column, Integer, DateTime, String, func, ForeignKey
from core.db import Base


class Tasks(Base):
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String())
    result = Column(String())
    periods = Column(Integer, ForeignKey('periods.id'))


class Periods(Base):
    task = Column(Integer, ForeignKey('tasks.id'))
    started_at = Column(DateTime(timezone=True), default=func.now())
    ended_at = Column(DateTime(timezone=True))