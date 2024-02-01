# from core.db import AsyncSessionLocal
# from models.user import User


# async def create_user(new_user: UserSchema) -> User:
#     new_user_data = new_user.dump_fields
#     user = User(**new_user_data)

#     async with AsyncSessionLocal() as session:
#         print('add')
#         session.add(user)
#         await session.commit()
#         await session.refresh(user)
#     return user



# from sqlalchemy import ForeignKey
# from typing import Optional
# from core.db import Base, CRUD
# from sqlalchemy.orm import Mapped, mapped_column, relationship


# class Telegram(Base, CRUD):
    
#     telegram_id: Mapped[int] = mapped_column(nullable=False, unique=True)
#     first_name: Mapped[Optional[str]]
#     last_name: Mapped[Optional[str]]
#     username: Mapped[Optional[str]]
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

#     user: Mapped["User"] = relationship("User", back_populates='telegram')
    

# __all__ = ['Telegram']