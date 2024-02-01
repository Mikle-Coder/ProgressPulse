from sqlalchemy import select
import json
from core.base import AsyncSessionLocal


class ModelCRUDMixin:
    @classmethod
    async def get(cls, **filters):
        async with AsyncSessionLocal() as session:
            db_objs = await session.execute(select(cls).filter_by(**filters))
            return db_objs.scalars().all()
    
    @classmethod
    async def get_first(cls, **filters):
        async with AsyncSessionLocal() as session:
            db_objs = await session.execute(select(cls).filter_by(**filters))
            return db_objs.scalars().first()

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

    
class SchemaCRUDMixin:
    @classmethod
    async def get(cls, **filters):
        return cls().load(cls.Meta.model.get(**filters))
    
    @classmethod
    async def get_first(cls, **filters):
        return cls().load(cls.Meta.model.get_first(**filters))

    @classmethod
    async def create(cls, obj):
        return cls().load(cls.Meta.model.create(obj))

    @classmethod
    async def update(cls, db_obj, obj_in):
        return cls().load(cls.Meta.model.update(db_obj, obj_in))

    @classmethod
    async def remove(cls, db_obj):
        return cls().load(cls.Meta.model.remove(db_obj))