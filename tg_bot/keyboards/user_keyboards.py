from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text = "Переслать голосовое", callback_data="my_voice"))
    kb.add(InlineKeyboardButton(text = "Персонажи", callback_data="pers"))
    kb.add(InlineKeyboardButton(text = "Купить войсы", callback_data="buy"))
    kb.add(InlineKeyboardButton(text = "Получить войсы", callback_data="reflink"))
    return kb

def subscribe_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Перейти в канал", url = "https://t.me/voicefusion"))
    kb.add(InlineKeyboardButton(text="Проверить подписку", callback_data="check_sub"))

def tohome_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Главное меню", callback_data="home"))
    return kb

def pers_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Бурунов", callback_data="curr_burunov"))
    kb.add(InlineKeyboardButton(text="Древний Рус", callback_data="curr_drevniy"))
    kb.add(InlineKeyboardButton(text="Зубарев", callback_data="curr_zubarev"))
    kb.add(InlineKeyboardButton(text="Меллстрой", callback_data="curr_melstroy"))
    kb.add(InlineKeyboardButton(text="Мистер Бист", callback_data="curr_beast"))
    kb.add(InlineKeyboardButton(text="Моргенштерн", callback_data="curr_morgen"))
    kb.add(InlineKeyboardButton(text="Мориарти", callback_data="curr_moriarty"))
    kb.add(InlineKeyboardButton(text="Морти", callback_data="curr_morty"))
    kb.add(InlineKeyboardButton(text="Нагиев", callback_data="curr_nagiev"))
    kb.add(InlineKeyboardButton(text="Главное меню", callback_data="home"))
    return kb