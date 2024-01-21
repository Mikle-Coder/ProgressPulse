from aiogram import types, filters, Router, F
from telegram_bot.keyboards.keyboard_start import kb_start
from schemas.telegram import Telegram, TelegramSchema
from models.user import User
from aiogram import types, filters, Router
from aiogram.fsm.context import FSMContext
from telegram_bot.states import state_task as st, state_result as sr
from telegram_bot.keyboards import names, keyboard_start, keyboard_process


rtr = Router()

@rtr.message(F.text == names.START)
async def process_start(message: types.Message, state: FSMContext):
    await state.set_state(st.StTask.task)
    await message.answer('Напиши задачу', reply_markup=types.ReplyKeyboardRemove())


@rtr.message(F.text == names.STOP)
async def process_stop(message: types.Message, state: FSMContext):
    await state.set_state(sr.StResult.result)
    await message.answer('Напиши результат', reply_markup=types.ReplyKeyboardRemove())


@rtr.message(F.text == names.PAUSE)
async def process_pause(message: types.Message):
    await message.answer('.', reply_markup=keyboard_process.kb_process_off)


@rtr.message(F.text == names.RESUME)
async def process_resume(message: types.Message):
    await message.answer('.', reply_markup=keyboard_process.kb_process_on)


@rtr.message(st.StTask.task)
async def process_task(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Задание получено', reply_markup=keyboard_process.kb_process_on)


@rtr.message(sr.StResult.result)
async def process_result(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Результат получен', reply_markup=keyboard_start.kb_start)