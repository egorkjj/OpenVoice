from aiogram import Dispatcher,types
from aiogram.dispatcher import FSMContext
from aiogram.types import LabeledPrice
from aiogram.types.message import ContentType
from tg_bot.keyboards import payment_keyboard, tohome_kb, pay_kb, back_promo, deeplink_kb, invoices_kb, howtopay, pay_yookassa_kb
from tg_bot.DBSM import up_voices, promo_info
from tg_bot.states import user
from aiogram.utils.deep_linking import get_start_link

def register_payment_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_payment, text = "buy")
    dp.register_callback_query_handler(promo, text="promo")
    dp.register_callback_query_handler(deeplinking, text="reflink")
    
    dp.register_callback_query_handler(send_invoice_stars, text_startswith = "invoice", state = "*")
    dp.register_callback_query_handler(send_invoice_yookassa, text_startswith = "yoinvoice", state = "*")

    dp.register_callback_query_handler(howtopay_proc, text_startswith = "pby")

    dp.register_callback_query_handler(promo_back, text="back", state = user.promo)
    dp.register_message_handler(promo_process, state=user.promo)

    dp.register_pre_checkout_query_handler(process_pre_checkout_query)
    dp.register_message_handler(succesfull_pay, content_types= ContentType.SUCCESSFUL_PAYMENT)

async def start_payment(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите, как вам будет удобнее оплатить 👇", reply_markup= howtopay())

async def howtopay_proc(call: types.CallbackQuery, state: FSMContext):
    if call.data.split("_")[1] == "stars":
        await call.message.answer("Выберите интересующий вас тариф 👇", reply_markup= payment_keyboard())
    else:
        await call.message.answer("Выберите интересующий вас тариф 👇", reply_markup= pay_yookassa_kb())

async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

async def send_invoice_stars(call: types.CallbackQuery, state: FSMContext):
    price = int(call.data.split("_")[2])
    amount = call.data.split("_")[1]

    prices = [LabeledPrice(label="XTR", amount=price)]  
    await call.message.bot.send_invoice(  
        title="Покупка войсов",  
        description=f"Пополнение баланса личного кабинета  на {amount} 🎙",  
        prices=prices,  
        provider_token="",  
        payload=f"{amount}",  
        currency="XTR",  
        reply_markup=pay_kb(price, True),  
        chat_id= call.message.chat.id,
        start_parameter="ru"
    )

async def send_invoice_yookassa(call: types.CallbackQuery, state: FSMContext):
    price = int(call.data.split("_")[2])
    amount = call.data.split("_")[1]

    prices = [LabeledPrice(label="RUB", amount=price)]  
    await call.message.bot.send_invoice(  
        title="Покупка войсов",  
        description=f"Пополнение баланса личного кабинета  на {amount} 🎙",  
        prices=prices,  
        provider_token="390540012:LIVE:53714",  
        payload=f"{amount}",  
        currency="RUB",  
        reply_markup=pay_kb(str(price)[:-2], False),  
        chat_id= call.message.chat.id,
        start_parameter="ru"
    )
   

async def send_pay(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        price = data["price"]
        amount = data["amount"]

    if call.data.split("_")[1] == "stars":
        prices = [LabeledPrice(label="XTR", amount=price)]  
        await call.message.bot.send_invoice(  
            title="Покупка войсов",  
            description=f"Пополнение баланса личного кабинета  на {amount} 🎙",  
            prices=prices,  
            provider_token="",  
            payload=f"{amount}",  
            currency="XTR",  
            reply_markup=pay_kb(price, True),  
            chat_id= call.message.chat.id,
            start_parameter="ru"
        )
    else:
        prices = [LabeledPrice(label="RUB", amount= price * 100)]  
        await call.message.bot.send_invoice(  
            title="Покупка войсов",  
            description=f"Пополнение баланса личного кабинета на {amount} 🎙",  
            prices=prices,  
            provider_token="390540012:LIVE:53714",  
            payload=f"{amount}",  
            currency="RUB",  
            reply_markup=pay_kb(price, False),  
            chat_id= call.message.chat.id,
            start_parameter="ru"
        )



async def succesfull_pay(message: types.Message, state: FSMContext):
    amount = int(message.successful_payment.invoice_payload)
    up_voices(message.chat.id, amount=amount)
    await message.answer(f"Счет вашего личного кабинета успешно пополнен на {amount} 🎙", reply_markup= tohome_kb())

async def deeplinking(call: types.CallbackQuery, state: FSMContext):
    link = await get_start_link(call.from_user.username, encode=True)
    await call.message.edit_text(text = f"Ваша реферальная ссылка _(нажмите на нее, и она сама скопируется)_:\n\n👉 `{link}`\n\n❗После первой озвучки друга -  _начислим 5🎙_", reply_markup= deeplink_kb(), parse_mode="markdown")

async def promo(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите промокод ниже 👇", reply_markup= back_promo())
    await user.promo.set()

async def promo_back(call: types.CallbackQuery, state: FSMContext):
    link = await get_start_link(call.from_user.username, encode=True)
    await call.message.edit_text(text = f"Ваша реферальная ссылка _(нажмите на нее, и она сама скопируется)_:\n\n👉 `{link}`\n\n❗После первой озвучки друга -  _начислим 5🎙_", reply_markup= deeplink_kb(), parse_mode="markdown")
    await state.finish()

async def promo_process(message: types.Message, state: FSMContext):
    result = promo_info(message.text, message.from_user.username)
    if not result[0]:
        await message.answer(result[1], reply_markup= tohome_kb())
    else:
        await message.answer(f"Баланс вашего аккаунта был пополнен на {result[1]}🎙", reply_markup= tohome_kb())
    await state.finish()
