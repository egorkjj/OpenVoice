from aiogram import Dispatcher,types
from aiogram.dispatcher import FSMContext

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])

async def cmd_start(message: types.Message, state: FSMContext):
    print(await message.bot.get_chat_member(chat_id="@fjhjfefhfjhefhk", user_id= message.from_user.id))
     