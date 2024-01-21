from core.db import AsyncSessionLocal
from models.user import User
from schemas.user import UserSchema


async def create_user(new_user: UserSchema) -> User:
    new_user_data = new_user.dump_fields
    user = User(**new_user_data)

    async with AsyncSessionLocal() as session:
        print('add')
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user