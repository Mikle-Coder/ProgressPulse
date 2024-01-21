from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker, scoped_session
from sqlalchemy import select, Column, Integer
import json
from sqlalchemy.exc import NoResultFound

from core.config import DATABASE_URL


engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
Session = scoped_session(AsyncSessionLocal)


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)


class CRUD:
    @classmethod
    async def get(cls, **filters):
        async with AsyncSessionLocal() as session:
            db_objs = await session.execute(select(cls).filter_by(**filters))
        return db_objs.scalars().all()

    @classmethod
    async def create(cls, obj):
        async with AsyncSessionLocal() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        return obj

    @classmethod
    async def update(cls, db_obj, obj_in):
        obj_data = json.dumps(db_obj, default=lambda o: o.__dict__)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        async with AsyncSessionLocal() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    @classmethod
    async def remove(cls, db_obj):
        async with AsyncSessionLocal() as session:
            await session.delete(db_obj)
            await session.commit()
        return db_obj
    
    @classmethod
    async def exists(cls, obj):
        async with AsyncSessionLocal() as session:
            filters = {field: getattr(obj, field) for field in obj.__dict__ if not field.startswith('_')}
            res = await session.execute(select(cls).filter_by(**filters))
            return bool(res.scalar())

    
Base = declarative_base(cls=PreBase)