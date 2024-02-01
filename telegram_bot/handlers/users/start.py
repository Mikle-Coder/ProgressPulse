from aiogram import types, filters, Router
from telegram_bot.keyboards.keyboard_start import kb_start
from telegram_bot.keyboards.keyboard_process import kb_process_off
from schemas.telegram import Telegram
from models.user import User
from models.task import Status
from core.db import Session


rtr = Router()


@rtr.message(filters.CommandStart())
async def cmd_start(message: types.Message):
    chat = message.chat
    keyboard = kb_start
    async with Session() as session:
        if user := await User.get_by_telegram_id(session, chat.id, False):
            text = 'C возвращением' + f', {user.telegram.first_name})' if user.telegram.first_name else ')'
            if user.current_task:
                text += '\n\nТекущая задача:\n' + user.current_task.description
                if user.current_task.status == Status.on_process:
                    await user.current_task.pause(session)
                keyboard = kb_process_off
        else:
            text = 'Добро пожаловать' + f', {chat.first_name})' if chat.first_name else ')'
            session.add(User(
                telegram=Telegram(
                    telegram_id=chat.id,
                    first_name=chat.first_name,
                    last_name=chat.last_name,
                    username=chat.username)
            )
            )
            await session.commit()
    await message.answer(text=text, reply_markup=keyboard)


    # if (await create_user(user)):
    #     await message.answer(
    #     text='---------🤖---------\n\n'
    #       'Приветсвую, я персональный помощник по учету задач в компании P.M.\n'
    #       'Чтобы начать задачу нажми кнопку Старт',
    #     reply_markup=kb_start
    # )
# @rtr.message_reaction()
# async def message_reaction_handler(message_reaction: types.MessageReactionUpdated):
#     reactions = message_reaction.new_reaction
#     await message_reaction.bot.send_message(message_reaction.chat.id, reactions[0].emoji)
