from aiogram.dispatcher.filters.state import State, StatesGroup

class user(StatesGroup):
    my_voice_voice = State()
    my_voice_text = State()
    pers_text = State()
    curr_text = State()
