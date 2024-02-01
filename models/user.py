from sqlalchemy import DateTime, func, ForeignKey, select, extract
from sqlalchemy.orm import relationship, Mapped, mapped_column, joinedload, selectinload, aliased
from core.db import Base, CRUD, AsyncSession
from datetime import datetime
from models.task import Period


class User(Base, CRUD):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    current_task_id: Mapped[int] = mapped_column(
        ForeignKey('task.id'), nullable=True)

    telegram: Mapped["Telegram"] = relationship(back_populates='user')
    tasks: Mapped[list["Task"]] = relationship(
        back_populates='user', primaryjoin='User.id==Task.user_id', post_update=True)
    current_task: Mapped["Task"] = relationship(
        foreign_keys=[current_task_id]
    )


    @classmethod
    async def get_by_telegram_id(cls, session, telegram_id, load_tasks=True) -> "User":
        options = (
            joinedload(cls.telegram),
            joinedload(cls.current_task),
            )
        options += (selectinload(cls.tasks),) if load_tasks else ()

        query = select(cls).options(*options).filter(cls.telegram.has(telegram_id=telegram_id))
        result = await session.execute(query)
        user = result.scalars().first()
        return user
    

    async def get_total_duration(self, session: AsyncSession) -> float:
        total_duration_query = select(func.coalesce(func.sum(
            extract('epoch', Period.ended_at) - 
            extract('epoch', Period.started_at)
        ), 0)).where(Period.task_id.in_([task.id for task in self.tasks]) & Period.ended_at.isnot(None))

        total_duration = (await session.execute(total_duration_query)).scalar()
        return total_duration


__all__ = ['User']
