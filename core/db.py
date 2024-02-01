from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import declared_attr, selectinload, Mapped, mapped_column, DeclarativeBase
from sqlalchemy import select
import json
from core.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
Session: AsyncSession = async_sessionmaker(engine, expire_on_commit=True)


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, sort_order=-1)

    def __repr__(self):
        W = '\033[0m'  # белый (нормальный)
        LB = '\033[35m'  # зеленый
        R = '\033[31m'  # красный
        B = '\033[34m'  # синий

        fields = " ".join(
            f'{B}{column.name}={LB}`{getattr(self, column.name)}`' for column in self.__table__.columns)
        return f'{R}{self.__class__.__name__} [{fields}{R}]{W}'


class CRUD:
    @classmethod
    async def get(cls, session, **filters):
        query = select(cls).filter_by(**filters).options(selectinload('*'))
        db_objs = await session.execute(query)
        return db_objs.scalars().all()

    @classmethod
    async def get_first(cls, **filters):
        async with Session() as session:
            query = select(cls).filter_by(**filters).options(selectinload('*'))
            db_objs = await session.execute(query)
            return db_objs.scalars().first()

    @classmethod
    async def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def update(cls, db_obj, obj_in):
        async with Session() as session:
            obj_data = json.dumps(db_obj, default=lambda o: o.__dict__)
            update_data = obj_in.dict(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    @classmethod
    async def remove(cls, db_obj):
        async with Session() as session:
            await session.delete(db_obj)
            await session.commit()
            return db_obj

    @classmethod
    async def exists(cls, obj):
        async with Session() as session:
            filters = {field: getattr(
                obj, field) for field in obj.__dict__ if not field.startswith('_')}
            res = await session.execute(select(cls).filter_by(**filters))
            return bool(res.scalar())


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)