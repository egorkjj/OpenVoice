from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType
from tg_bot.keyboards import admin_kb, token_kb
from tg_bot.DBSM import all_user_list, bonus, add_promo, all_promo, all_token, add_token, rm_token
from tg_bot.states import admin

admin_ids = [441487518,861756342,759553639,1441962095, 759553639]
def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(start_admin, lambda message: message.chat.id in admin_ids, commands=["admin"], state = "*")
    dp.register_callback_query_handler(admin_proc, text_startswith = "admin")

    dp.register_message_handler(rassylka, state = admin.text_rass, content_types= ContentType.ANY)

    dp.register_message_handler(bonus_step1, state= admin.username)
    dp.register_message_handler(bonus_step2, state= admin.bonus)

    dp.register_message_handler(promo_step1, state = admin.promo_name)
    dp.register_message_handler(promo_step2, state = admin.promo_act)
    dp.register_message_handler(promo_step3, state = admin.promo_gift)

    dp.register_message_handler(token_proc, state = admin.token)
    dp.register_message_handler(rmtoken_proc, state = admin.rmtoken)


async def start_admin(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Здравствуйте! Что Вы хотите сделать?", reply_markup=admin_kb())

async def admin_proc(call: types.CallbackQuery, state: FSMContext):
    action = call.data.split("_")[1]
    if action == "users":
        users = all_user_list()
        usersAlive = []
        waitmsg = await call.message.answer('Подготовка статистики. Это может занять некоторе время...')
        for user in users:
            try:
                await call.message.bot.send_chat_action(call.message.chat.id, "TYPING")
                usersAlive.append(user.chat_id)
            except:
                pass
            usersDead = len(set(users))-len(set(usersAlive))
            await waitmsg.delete()
            await call.message.answer(f"""
                <b>Статистика</b>👤 Всего пользователей: {str(len(users))}\n🟢 Активных пользователей: {str(len(usersAlive))}\n🔴 Неактивных пользователей: {str(usersDead)}
            """)
        
    elif action == "rassylka":
        await admin.text_rass.set()
        await call.message.answer("Введите текст рассылки")
    elif action == "bonus":
        await admin.username.set()
        await call.message.answer("Введите юзернейм пользователя, которому хотите выдать валюту")
    elif action == "promo":
        await admin.promo_name.set()
        await call.message.answer("Введите промокод")
    elif action == "tokens":
        text = ""
        res = all_token()
        for i in res:
            text += f"Токен: <b>{i['token']}</b>, <b>нерабочий ❌</b>\n" if not i["is_used"] else f"Токен: <b>{i['token']}</b>, <b>осталось активаций: {i['usage']}</b>\n"  
        await call.message.answer(text, reply_markup= token_kb())
    elif action == "addtoken":
        await call.message.answer("Введите токен")
        await admin.token.set()
    elif action == "rmtoken":
        await call.message.answer("Введите токен")
        await admin.rmtoken.set()
    else:
        res = all_promo()
        text = "Промокоды:\n"
        for i in res:
            text += f"название: <b>{i.name}</b>, активаций осталось: <b>{i.activations}</b>, кол-во валюты за активацию: <b>{i.gift}</b>\n"
        await call.message.answer(text)


async def token_proc(message: types.Message, state: FSMContext):
    add_token(message.text)
    await message.answer("Токен добавлен")
    await state.finish()

async def rmtoken_proc(message: types.Message, state: FSMContext):
    rm_token(message.text)
    await message.answer("Токен удален")
    await state.finish()

async def rassylka(message: types.Message, state: FSMContext):
    await message.answer("Рассылка произведена")
    lis = all_user_list()
    for i in lis:
        await message.send_copy(i.chat_id)
    await state.finish()


async def bonus_step1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["username"] = message.text.replace("@", "")
    await admin.bonus.set()
    await message.answer("Введите количество 🎙, которое хотите выдать пользователю")

async def bonus_step2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        bonus(data["username"], message.text)
    await message.answer(f"Пользователю {data['username']} выдано {message.text} 🎙")
    await state.finish()


async def promo_step1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["promo_name"] = message.text
    await admin.promo_act.set()
    await message.answer("Введите количество активаций промокода")

async def promo_step2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["promo_act"] = int(message.text)
    await admin.promo_gift.set()
    await message.answer("Теперь введите количество валюты, которое будет даваться за активацию")

async def promo_step3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        add_promo(data["promo_name"], data["promo_act"], int(message.text))
    await message.answer("Промокод добавлен")
    await state.finish()


    