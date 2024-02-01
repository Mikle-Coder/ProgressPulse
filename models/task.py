from sqlalchemy import DateTime, func, ForeignKey, select, extract
from core.db import Base, AsyncSession
from sqlalchemy.orm import relationship, mapped_column, Mapped
import enum
from datetime import datetime


class Status(enum.Enum):
    created = "created"
    on_process = "on_process"
    paused = "paused"
    finished = "finished"


class Result(Base):
    task_id: Mapped[int] = mapped_column(
        ForeignKey('task.id', ondelete='CASCADE'))
    text: Mapped[str]


class Period(Base):
    task_id: Mapped[int] = mapped_column(
        ForeignKey('task.id', ondelete='CASCADE'))
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True)


class Task(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'))
    description: Mapped[str]
    status: Mapped[Status] = mapped_column(
        default=Status.created)
    extra_time: Mapped[int] = mapped_column(server_default='0')

    user: Mapped["User"] = relationship(
        foreign_keys=[user_id], back_populates='tasks')
    result: Mapped["Result"] = relationship()
    periods: Mapped[list["Period"]] = relationship()


    async def pause(self, session: AsyncSession):
        query = select(Period).filter_by(task_id=self.id).order_by(Period.id.desc()).limit(1)
        period = (await session.execute(query)).scalars().one()
        period.ended_at = func.now()
        self.status = Status.paused
        await session.commit()

    async def resume(self, session: AsyncSession):
        session.add(Period(task_id=self.id))
        self.status = Status.on_process
        await session.commit()

    async def stop(self, session: AsyncSession):
        if self.status == Status.on_process:
            query = select(Period).filter_by(task_id=self.id).order_by(Period.id.desc()).limit(1)
            period = (await session.execute(query)).scalars().one()
            period.ended_at = func.now()
        self.status = Status.finished
        await session.commit()

    async def get_duration(self, session: AsyncSession) -> float:
        query = select(func.sum(
             func.ifnull(
            extract('epoch', Period.ended_at),
            extract('epoch', func.now())) - 
            extract('epoch', Period.started_at)
            )
        ).where(Period.task_id == self.id)

        total_duration = (await session.execute(query)).scalar()
        return total_duration + self.extra_time


__all__ = ['Status', 'Result', 'Period', 'Task']
