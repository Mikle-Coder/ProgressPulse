from aiogram.fsm.state import StatesGroup, State


class StReg(StatesGroup):
    nickname = State()