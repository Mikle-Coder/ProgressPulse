from aiogram.fsm.state import StatesGroup, State


class StTask(StatesGroup):
    task = State()