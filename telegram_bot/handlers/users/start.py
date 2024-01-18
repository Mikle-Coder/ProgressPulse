from aiogram import types, filters, Router
from ...keyboards.keyboard_start import kb_start


rtr = Router()

@rtr.message(filters.CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        text='---------🤖---------\n\n'
          'Приветсвую, я персональный помощник по учету задач в компании P.M.\n'
          'Чтобы начать задачу нажми кнопку Старт',
        reply_markup=kb_start
    )

# @rtr.message_reaction()
# async def message_reaction_handler(message_reaction: types.MessageReactionUpdated):
#     reactions = message_reaction.new_reaction
#     await message_reaction.bot.send_message(message_reaction.chat.id, reactions[0].emoji)