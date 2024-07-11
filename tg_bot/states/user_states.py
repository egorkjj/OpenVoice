from aiogram.dispatcher.filters.state import State, StatesGroup

class user(StatesGroup):
    my_voice_voice = State()
    my_voice_text = State()
    pers_text = State()
    curr_text = State()
    promo = State()

class admin(StatesGroup):
    text_rass = State()
    username = State()
    bonus = State()
    promo_name = State()
    promo_act = State()
    promo_gift = State()
    token = State()
