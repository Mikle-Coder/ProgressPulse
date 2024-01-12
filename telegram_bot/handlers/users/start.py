from aiogram import types, filters
from loader import dp


@dp.message(filters.CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Привет {message.from_user.full_name}! \n"
                         f"Твой id: {message.from_user.id}"
                         )