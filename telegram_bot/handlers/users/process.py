from datetime import timedelta, datetime
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import bold
from core.db import Session
from core.config import BOT_TOKEN
from models.task import Task, Period, Status, Result
from models.user import User
from telegram_bot.states import state_task as st, state_result as sr
from telegram_bot.keyboards import names, keyboard_start, keyboard_process
from telegram_bot.utils.task_timer import task_timer


rtr = Router()


@rtr.message(F.text == names.START)
async def process_start(message: types.Message, state: FSMContext):
    async with Session() as session:
        user = await User.get_by_telegram_id(session, message.chat.id)
        if user.current_task:
            return
    await state.set_state(st.StTask.task)
    await message.answer('✴️ Напиши свою задачу, которую будешь выполнять', reply_markup=types.ReplyKeyboardRemove())


@rtr.message(F.text == names.STOP)
async def process_stop(message: types.Message, state: FSMContext):
    async with Session() as session:
        user = await User.get_by_telegram_id(session, message.chat.id)
        print(user.current_task, user.current_task.status)
        if user.current_task and user.current_task.status != Status.finished:
            await user.current_task.stop(session)
            await state.set_state(sr.StResult.result)
            await message.answer('⭕️ Напиши свой результат', reply_markup=types.ReplyKeyboardRemove())


@rtr.message(F.text == names.PAUSE)
async def process_pause(message: types.Message):
    async with Session() as session:
        user = await User.get_by_telegram_id(session, message.chat.id)
        if user.current_task and user.current_task.status == Status.on_process:
            await task_timer.remove_task(user.current_task.id)
            await user.current_task.pause(session)
            await message.answer('⚠️ Задача приостановлена', reply_markup=keyboard_process.kb_process_off)


@rtr.message(F.text == names.RESUME)
async def process_resume(message: types.Message):
    async with Session() as session:
        user = await User.get_by_telegram_id(session, message.chat.id)
        if user.current_task and user.current_task.status == Status.paused:
            await task_timer.add_task(user.current_task.id, datetime.utcnow())
            await user.current_task.resume(session)
            await message.answer('✳️ Задача возобновлена', reply_markup=keyboard_process.kb_process_on)


@rtr.message(st.StTask.task)
async def process_task(message: types.Message, state: FSMContext):
    await state.clear()
    async with Session() as session:
        user = await User.get_by_telegram_id(session, message.chat.id)
        task = Task(
            user_id=user.id,
            description=message.text,
            periods=[Period()],
            status=Status.on_process
            )
        user.current_task = task
        session.add(user)
        await session.commit()
        await session.refresh(user)
        await task_timer.add_task(user.current_task.id, datetime.utcnow())

    await message.answer('✳️ Задание получено, время пошло', reply_markup=keyboard_process.kb_process_on)


@rtr.message(sr.StResult.result)
async def process_result(message: types.Message, state: FSMContext):
    await state.clear()
    async with Session() as session:
        user = await User.get_by_telegram_id(session, message.chat.id)
        user.current_task.result = Result(text=message.text)
        duration = timedelta(seconds=await user.current_task.get_duration(session))
        user.current_task = None
        await session.commit()
        await message.answer('✅ Ты выполнил задание за: ' + bold(duration), reply_markup=keyboard_start.kb_start)


async def task_timeout(task_id):
    async with Session() as session:
        query = select(Task).options(
            joinedload(Task.user).joinedload(User.telegram)
        ).filter_by(id=task_id)
        task: Task = (await session.execute(query)).scalars().first()
        if task.status == Status.on_process:
            bot = Bot(BOT_TOKEN)
            from aiogram.enums import ParseMode
            await bot.send_message(task.user.telegram.telegram_id, '⚠️ Время ожидания вышло, я поставлю выполнение на паузу', parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_process.kb_process_off)
            await task.pause(session)