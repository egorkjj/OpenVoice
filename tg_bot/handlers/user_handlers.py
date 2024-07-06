from aiogram import Dispatcher,types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from tg_bot.keyboards import start_kb, subscribe_kb, tohome_kb, pers_kb, sell_kb, deeplink_kb
from tg_bot.DBSM import get_voices, minus_voice, add_new, get_voices_string
from tg_bot.states import user
from tg_bot.neiro import OpenVoice
import os, string, random

from aiogram.utils.deep_linking import get_start_link, decode_payload

names_js = {
    "markaryan": "Маркарян",
    "putin": "Путин",
    "burunov": "Бурунов",
    "moriarty": "Мориарти",
    "prigozhin": "Пригожин",
    "drevniy": "Древний Рус"
}
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"], state = None)
    dp.register_message_handler(my_voice_step1, content_types=types.ContentType.VOICE, state = user.my_voice_voice)
    dp.register_message_handler(my_voice_step2, state = user.my_voice_text)
    dp.register_message_handler(pers_final, state = user.curr_text)

    dp.register_callback_query_handler(pers_choice, text_startswith = "curr", state = None)
    dp.register_callback_query_handler(check_sub, text="check_sub", state = None)
    dp.register_callback_query_handler(my_voice, text="my_voice", state = None)
    dp.register_callback_query_handler(pers, text="pers", state = None)
    dp.register_callback_query_handler(home, text="home", state = "*")


async def cmd_start(message: types.Message, state: FSMContext): #start command
    args = message.get_args()
    reference = decode_payload(args)
    add_new(message, reference)
    voices = get_voices_string(message.chat.id)
    await message.answer(f"🎁 Разыграйте друзей, озвучив текст любым голосом!\n\n🎤 Воспользуйтесь озвучкой по персонажам или просто отправьте мне любое голосовое сообщение!\n\nБаланс: {voices} 🎙\nУ вас стандартный доступ к боту 👨‍💻\n\nОбновления и бесплатные войсы в нашем канале 👉 @voicefusion", reply_markup= start_kb())


async def subscriber_check(id, msg: types.Message): #проверка на то, саб ли человек - НЕ ХЭНДЛЕР!!!!
    data = await msg.bot.get_chat_member(chat_id="@fjhjfefhfjhefhk", user_id= id)
    print(data["status"])
    res = data["status"] != "left"
    if not res:
        await msg.answer("Для продолжения работы в боте, подпишитесь на наш канал @voicefusion", reply_markup= subscribe_kb())
        return False
    else:
        return True
    

async def home(call: types.CallbackQuery, state: FSMContext): #tohome
    if await state.get_state() != "user:my_voice_text":
        await state.finish()
    voices = get_voices_string(call.message.chat.id)
    await call.message.edit_text(f"🎁 Разыграйте друзей, озвучив текст любым голосом!\n\n🎤 Воспользуйтесь озвучкой по персонажам или просто отправьте мне любое голосовое сообщение!\n\nБаланс: {voices} 🎙\nУ вас стандартный доступ к боту 👨‍💻\n\nОбновления и бесплатные войсы в нашем канале 👉 @voicefusion", reply_markup= start_kb())


async def check_sub(call: types.CallbackQuery, state: FSMContext): #check sub from reply_markup
    data = await call.message.bot.get_chat_member(chat_id="@fjhjfefhfjhefhk", user_id= call.from_user.id)
    if data["status"] != "left":
        await call.message.edit_text("Благодарим за подписку. Теперь можно продолжить)", reply_markup=None)
        voices = get_voices_string(call.message.chat.id)
        await call.message.answer(f"🎁 Разыграйте друзей, озвучив текст любым голосом!\n\n🎤 Воспользуйтесь озвучкой по персонажам или просто отправьте мне любое голосовое сообщение!\n\nБаланс: {voices} 🎙\nУ вас стандартный доступ к боту 👨‍💻\n\nОбновления и бесплатные войсы в нашем канале 👉 @voicefusion", reply_markup= start_kb())
    else:
        await call.message.edit_text("К сожалению, вы еще не подписаны(\nДля продолжения работы в боте, подпишись на наш канал @voicefusion", reply_markup=subscribe_kb())



async def my_voice(call: types.CallbackQuery, state: FSMContext):
    if not await subscriber_check(call.from_user.id, call.message):
        return
    voices = get_voices_string(call.message.chat.id)
    await call.message.edit_text(f"Перешлите мне голосовое сообщение от 5 секунд до 3 минут и я сделаю речевую модель на его основе 🔉\n\nВаш баланс: {voices}🎙\nОдна генерация по голосовому: 6🎙", reply_markup=tohome_kb())
    await user.my_voice_voice.set()

async def my_voice_step1(message: types.Message, state: FSMContext):
    if get_voices(message.chat.id) < 6:
        await message.answer("К сожалению, у вас недостаточно войсов ❌", reply_markup= sell_kb())
        await state.finish()
        return
    if message.voice.duration < 5 or message.voice.duration > 180:
        await message.answer("мГолосовое должно быть от 5 секунд до 3 минут❗")
        return
    
    def generate_random_string(length):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    if not os.path.isdir("tg_bot/user_models"):
        os.mkdir("tg_bot/user_models")

    name = generate_random_string(20) + ".wav"
    async with state.proxy() as data:
        data["name"] = f"tg_bot/user_models/{name}"
    await message.voice.download(f"tg_bot/user_models/{name}")
    await message.answer("Хорошо, теперь пришлите мне текст для озвучки длиной не менее 10 и не более 300 символов 👇")
    await user.my_voice_text.set()
    minus_voice(message.chat.id, 6)


async def my_voice_step2(message: types.Message, state: FSMContext):
    if len(message.text) < 10 or len(message.text) > 300:
        await message.answer("❗Длина сообщения должна быть не менее 10 и не более 300 символов❗")
        return
    await state.finish()
    async with state.proxy() as data:
        res = await OpenVoice(data["name"], message.text)
        with open(res, "rb") as voice:
            await message.bot.send_voice(voice = voice, chat_id= message.chat.id)
    



async def pers(call: types.CallbackQuery, state: FSMContext):
    if not await subscriber_check(call.from_user.id, call.message):
        return
    
    voices = get_voices_string(call.message.chat.id)

    await call.message.edit_text(f"Выбери интересующую речевую модель ниже 🗣️\n\nВаш баланс: {voices} 🎙\nОдна генерация: 1🎙", reply_markup= pers_kb())

async def pers_choice(call: types.CallbackQuery, state: FSMContext):
    name = call.data.split("_")[1]
    names = names_js[name]
    async with state.proxy() as data:
        data["pers"] = f"tg_bot/models/{name}.wav"
    await call.message.edit_text(f"Выбран персонаж: <b>{names}</b>\nТеперь пришлите мне текст для озвучки длиной не менее 10 и не более 300 символов 👇", reply_markup= tohome_kb())
    await user.curr_text.set()

async def pers_final(message: types.Message, state: FSMContext):
    if get_voices(message.chat.id) < 1:
        await message.answer("К сожалению, у вас недостаточно войсов ❌", reply_markup= sell_kb())
        await state.finish()
        return
    
    if len(message.text) < 10 or len(message.text) > 300:
        await message.answer("❗Длина сообщения должна быть не менее 10 и не более 300 символов❗")
        return
    
    async with state.proxy() as data:
        pers = data["pers"]
    await state.finish()
    minus_voice(message.chat.id, 1)
    res = await OpenVoice(pers, message.text)
    await message.bot.send_voice(voice = InputFile(res[0]), chat_id= message.chat.id, duration= res[1])


