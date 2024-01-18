from aiogram import types, filters, Router
from aiogram.fsm.context import FSMContext
from ...states.state_register import StReg


rtr = Router(name='nickname')

@rtr.message(filters.Command('nickname'))
async def cmd_register(message: types.Message, state: FSMContext):
    await state.set_state(StReg.nickname)
    await message.answer('Напиши свой новый Никнейм')


@rtr.message(StReg.nickname)
async def register_nickname(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f'Готово! \nТеперь я к тебе буду обращаться {message.text} 😉')
    print(message.text)