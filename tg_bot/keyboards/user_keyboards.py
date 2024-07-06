from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text = "Переслать голосовое 🗣️", callback_data="my_voice"))
    kb.add(InlineKeyboardButton(text = "Персонажи 👤", callback_data="pers"))
    kb.add(InlineKeyboardButton(text = "Купить войсы 💵", callback_data="buy"))
    kb.add(InlineKeyboardButton(text = "Получить войсы ➕ ", callback_data="reflink"))
    return kb

def subscribe_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Перейти в канал", url = "https://t.me/voicefusion"))
    kb.add(InlineKeyboardButton(text="Проверить подписку ✅", callback_data="check_sub"))
    return kb
def tohome_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Главное меню 🏠", callback_data="home"))
    return kb

def pers_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Бурунов 👤", callback_data="curr_burunov"))
    kb.add(InlineKeyboardButton(text="Древний Рус 👤", callback_data="curr_drevniy"))
    kb.add(InlineKeyboardButton(text="Мориарти 👤", callback_data="curr_moriarty"))
    kb.add(InlineKeyboardButton(text="Маркарян 👤", callback_data="curr_markaryan"))
    kb.add(InlineKeyboardButton(text="Путин 👤", callback_data="curr_putin"))
    kb.add(InlineKeyboardButton(text="Пригожин 👤", callback_data="curr_prigozhin"))
    kb.add(InlineKeyboardButton(text="Главное меню 🏠", callback_data="home"))
    return kb

def payment_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Купить 20 🎙 за 1 🌟", callback_data= "invoice_20_1"))
    kb.add(InlineKeyboardButton(text="Купить 50 🎙 за 2 🌟", callback_data="invoice_50_2"))
    kb.add(InlineKeyboardButton(text="Главное меню 🏠", callback_data="home"))
    kb.add(InlineKeyboardButton(text = "Получить войсы ➕ ", callback_data="reflink"))
    return kb

def pay_kb(price):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text=f"Заплатить {price} 🌟", pay = True))
    return kb

def sell_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text = "Купить войсы 💵", callback_data="buy"))
    kb.add(InlineKeyboardButton(text = "Получить войсы ➕ ", callback_data="reflink"))
    kb.add(InlineKeyboardButton(text="Главное меню 🏠", callback_data="home"))
    return kb

def deeplink_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text = "Купить войсы 💵", callback_data="buy"))
    kb.add(InlineKeyboardButton(text="Главное меню 🏠", callback_data="home"))
    kb.add(InlineKeyboardButton(text="У меня есть промокод 🎁", callback_data="promo"))
    return kb

def back_promo():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Назад 🔙", callback_data="back"))
    return kb

def admin_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Просмотреть количество пользователей", callback_data="admin_users"))
    kb.add(InlineKeyboardButton(text="Рассылка по пользователям", callback_data="admin_rassylka"))
    kb.add(InlineKeyboardButton(text="Добавить промокод", callback_data="admin_promo"))
    kb.add(InlineKeyboardButton(text="Начислением 🎙 пользователям", callback_data="admin_bonus"))
    kb.add(InlineKeyboardButton(text="Все промокоды", callback_data="admin_promos"))

    return kb

