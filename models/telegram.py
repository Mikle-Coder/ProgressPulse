from sqlalchemy import ForeignKey, select, exists
from typing import Optional
from core.db import Base, CRUD, AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload,  selectinload


class Telegram(Base, CRUD):

    telegram_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped["User"] = relationship("User", back_populates='telegram')

    @classmethod
    async def get(cls, session: AsyncSession, telegram_id: int):
        query = select(cls).options(
            joinedload(cls.user)
        ).filter_by(telegram_id=telegram_id)
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def exists(cls, session: AsyncSession, telegram_id: int):
        query = select(exists().where(cls.telegram_id == telegram_id))
        return await session.scalar(query)

    @classmethod
    async def get_user(cls, session: AsyncSession, telegram_id: int):
        obj = await cls.get(session, telegram_id)


__all__ = ['Telegram']
