from aiogram import Dispatcher,types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from tg_bot.keyboards import start_kb, subscribe_kb, tohome_kb, pers_kb
from tg_bot.DBSM import get_voices, minus_voice
from tg_bot.states import user
from tg_bot.neiro import OpenVoice
import os, string, random

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"], state = None)
    dp.register_message_handler(my_voice_step1, content_types=types.ContentType.VOICE, state = user.my_voice_voice)
    dp.register_message_handler(my_voice_step2, state = user.my_voice_text)

    dp.register_callback_query_handler(pers_choice, text_startswith = "curr")
    dp.register_callback_query_handler(check_sub, text="check_sub", state = None)
    dp.register_callback_query_handler(my_voice, text="my_voice", state = None)
    dp.register_callback_query_handler(pers, text="pers", state = None)
    dp.register_callback_query_handler(home, text="hone", state = "*")

async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("🎁 Разыграйте друзей, озвучив текст любым голосом!\n\n🎤 Воспользуйтесь озвучкой по персонажам или просто отправьте мне любое голосовое сообщение!\n\nБаланс: 10 Войсов 🎙\nУ вас стандартный доступ к боту 👨‍💻\n\nОбновления и бесплатные войсы в нашем канале 👉 @voicefusion", reply_markup= start_kb())

async def subscriber_check(msg: types.Message):
    data = await msg.bot.get_chat_member(chat_id="@fjhjfefhfjhefhk", user_id= msg.from_user.id)
    res = data["status"] != "left"
    if not res:
        await msg.answer("Для продолжения работы в боте, подпишись на наш канал @voicefusion", reply_markup= subscribe_kb())
        return False
    else:
        return True
    
async def home(call: types.CallbackQuery, state: FSMContext):
    if await state.get_state() != "user:my_voice_text":
        await state.finish()
    await call.message.edit_text("🎁 Разыграйте друзей, озвучив текст любым голосом!\n\n🎤 Воспользуйтесь озвучкой по персонажам или просто отправьте мне любое голосовое сообщение!\n\nБаланс: 10 Войсов 🎙\nУ вас стандартный доступ к боту 👨‍💻\n\nОбновления и бесплатные войсы в нашем канале 👉 @voicefusion", reply_markup= start_kb())

async def check_sub(call: types.CallbackQuery, state: FSMContext):
    data = await call.message.bot.get_chat_member(chat_id="@fjhjfefhfjhefhk", user_id= call.message.from_user.id)
    if data["status"] != "left":
        await call.message.edit_text("Благодарим за подписку. Теперь можно продолжить)", reply_markup=None)
        await call.message.answer("🎁 Разыграйте друзей, озвучив текст любым голосом!\n\n🎤 Воспользуйтесь озвучкой по персонажам или просто отправьте мне любое голосовое сообщение!\n\nБаланс: 10 Войсов 🎙\nУ вас стандартный доступ к боту 👨‍💻\n\nОбновления и бесплатные войсы в нашем канале 👉 @voicefusion", reply_markup= start_kb())
    else:
        await call.message.edit_text("Еще не подписан.\nДля продолжения работы в боте, подпишись на наш канал @VoicerAi", reply_markup=subscribe_kb())



async def my_voice(call: types.CallbackQuery, state: FSMContext):
    voices = get_voices(call.message.chat.id)
    await call.message.edit_text(f"Перешли мне голосовое сообщение от 5 секунд до 3 минут и я сделаю речевую модель на его основе 🔉\n\nВаш баланс: {voices}🎙\nОдна генерация по голосовому: 6🎙", reply_markup=tohome_kb())
    await user.my_voice_voice.set()


async def my_voice_step1(message: types.Message, state: FSMContext):
    if get_voices(message.chat.id) < 6:
        await message.answer("К сожалению, у тебя недостаточно войсов(")
        await state.finish()
        return
    if message.voice.duration < 5 or message.voice.duration > 180:
        await message.answer("Голосовое должно быть от 5 секунд до 3 минут")
        return
    
    def generate_random_string(length):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    if not os.path.isdir("tg_bot/voices"):
        os.mkdir("tg_bot/voices")

    name = generate_random_string(20) + ".wav"
    async with state.proxy() as data:
        data["name"] = name
    await message.voice.download(f"tg_bot/voices/{name}")
    await message.answer("Хорошо, теперь пришли текст для озвучки. Длина должна быть не менее 10 и не более 300 символов")
    await user.my_voice_text.set()
    minus_voice(message.chat.id, 6)

async def my_voice_step2(message: types.Message, state: FSMContext):
    if len(message.text) < 10 or len(message.text) > 300:
        await message.answer("Длина сообщения должна быть не менее 10 и не более 300 символов!")
        return
    async with state.proxy() as data:
        res = OpenVoice(data["name"], message.text)
        await message.answer_voice(voice = InputFile(res))
        await state.finish()
    


async def pers(call: types.CallbackQuery, state: FSMContext):
    voices = get_voices(call.message.chat.id)
    await call.message.edit_text(f"Выбери доступную модель озвучки по кнопкам ниже 🥷\n\nВаш баланс: {voices}🎙\nОдна генерация: 1🎙", reply_markup= pers_kb())

async def pers_choice(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1]
    async with state.proxy() as data:
        data["proxy"] = data

    


