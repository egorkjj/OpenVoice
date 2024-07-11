from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text = "Переслать голосовое 🗣️", callback_data="my_voice"))
    kb.add(InlineKeyboardButton(text = "Персонажи 👤", callback_data="pers"))
    kb.add(InlineKeyboardButton(text = "Купить войсы 💵", callback_data="buy"))
    kb.add(InlineKeyboardButton(text = "Получить войсы ➕ ", callback_data="reflink"))
    kb.add(InlineKeyboardButton(text = "Правила 📝", callback_data= "rules"))
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
    kb = InlineKeyboardMarkup(row_width=2)
    kb.row(InlineKeyboardButton(text="Бурунов 👤", callback_data="curr_burunov"), InlineKeyboardButton(text="Древний Рус 👤", callback_data="curr_drevniy"))
    # kb.add(InlineKeyboardButton(text="Бурунов 👤", callback_data="curr_burunov"))
    # kb.add(InlineKeyboardButton(text="Древний Рус 👤", callback_data="curr_drevniy"))
    kb.row(InlineKeyboardButton(text="Мориарти 👤", callback_data="curr_moriarty"), InlineKeyboardButton(text="Маркарян 👤", callback_data="curr_markaryan"))
    # kb.add(InlineKeyboardButton(text="Мориарти 👤", callback_data="curr_moriarty"))
    # kb.add(InlineKeyboardButton(text="Маркарян 👤", callback_data="curr_markaryan"))
    kb.row(InlineKeyboardButton(text="Путин 👤", callback_data="curr_putin"), InlineKeyboardButton(text="Пригожин 👤", callback_data="curr_prigozhin"))
    # kb.add(InlineKeyboardButton(text="Путин 👤", callback_data="curr_putin"))
    # kb.add(InlineKeyboardButton(text="Пригожин 👤", callback_data="curr_prigozhin"))
    kb.add(InlineKeyboardButton(text="Главное меню 🏠", callback_data="home"))
    return kb

def payment_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Купить 6 🎙 за 50 🌟", callback_data= "invoice_6_50"))
    kb.add(InlineKeyboardButton(text="Купить 10 🎙 за 75 🌟", callback_data= "invoice_10_75"))
    kb.add(InlineKeyboardButton(text="Купить 50 🎙 за 250 🌟", callback_data= "invoice_50_250"))
    kb.add(InlineKeyboardButton(text="Купить 200 🎙 за 750 🌟", callback_data= "invoice_200_750"))
    kb.add(InlineKeyboardButton(text="Купить 1000 🎙 за 2500 🌟", callback_data= "invoice_1000_2500"))
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

