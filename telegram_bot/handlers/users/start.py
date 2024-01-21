from aiogram import types, filters, Router
from telegram_bot.keyboards.keyboard_start import kb_start
from schemas.telegram import Telegram, TelegramSchema
from models.user import User


rtr = Router()

@rtr.message(filters.CommandStart())
async def cmd_start(message: types.Message):
    tg_user = message.chat
    schema = TelegramSchema()
    telegram = schema.load(tg_user.__dict__)

    if await Telegram.exists(telegram):
        text = 'С возвращением)'
    else:
        telegram.user = User()
        await Telegram.create(telegram)
        text = 'Добро пожаловать)'

    await message.answer(text=text, reply_markup=kb_start)





    # db.add(user)
    # await db.commit()
    # await db.refresh(user)


    # if (await create_user(user)):
    #     await message.answer(
    #     text='---------🤖---------\n\n'
    #       'Приветсвую, я персональный помощник по учету задач в компании P.M.\n'
    #       'Чтобы начать задачу нажми кнопку Старт',
    #     reply_markup=kb_start
    #)
# @rtr.message_reaction()
# async def message_reaction_handler(message_reaction: types.MessageReactionUpdated):
#     reactions = message_reaction.new_reaction
#     await message_reaction.bot.send_message(message_reaction.chat.id, reactions[0].emoji)
      