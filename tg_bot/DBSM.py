from sqlalchemy import create_engine, Column, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from aiogram.types import Message

DATABASE_URL = f"sqlite:///db.sqlite3"

# Создание объекта Engine
engine = create_engine(DATABASE_URL)

# Создание базового класса для моделей
Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(Text, nullable=True, unique=True)
    chat_id = Column(Text, nullable=True, unique=True)
    voices = Column(Integer, nullable=True)
    referal = Column(Text, nullable=True)
    is_ref_voices = Column(Boolean, nullable=True)

class Promos(Base):
    __tablename__ = "promos"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=True, unique=True)
    activations = Column(Integer, nullable=True)
    gift = Column(Integer, nullable=True)

def add_new(message: Message, referal):
    Session = sessionmaker()
    session = Session(bind = engine)
    try:
        new = User(username = message.from_user.username, chat_id = message.chat.id, voices = 10, is_ref_voices = False)
        session.add(new)
        session.commit()
    except:
        pass
    session.close()

def get_voices(chat_id):
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(User).filter(User.chat_id == chat_id).first()
    res = curr.voices
    session.close()
    return res

def minus_voice(chat_id, voices):
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(User).filter(User.chat_id == chat_id).first()
    curr.voices = curr.voices - voices
    session.commit()
    if not curr.is_ref_voices:
        referal = session.query(User).filter(User.username == curr.referal).first()
        if referal is not None:
            ref_v = referal.voices
            referal.voices = ref_v + 5
            session.commit()
    session.close()

def get_voices_string(chat_id):
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(User).filter(User.chat_id == chat_id).first()
    res = curr.voices
    session.close()
    if res % 10 == 1:
        return "1 войс"
    elif res % 10 in [2, 3, 4]:
        return f"{res} войса"
    else:
        return f"{res} войсов"
    

def up_voices(chat_id, amount: int):
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(User).filter(User.chat_id == chat_id).first()
    res = curr.voices
    curr.voices = res + amount
    session.commit()
    session.close()

def promo_info(promo, username):
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(Promos).filter(Promos.name == promo).first()
    if curr is None:
        session.close()
        return [False, "К сожкалению, такого промокода не существует("]
    elif curr.activations == 0:
        session.close()
        return [False, "К сожалению, у этого промокода закончились активации("]
    else:
        gift = curr.gift
        curr_user = session.query(User).filter(User.username == username).first()
        curr_user.voices = curr_user.voices + gift
        session.commit()
        session.close()
        return [True, gift]
    
def all_users():
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = len(session.query(User).all())
    session.close()
    return curr

def all_user_list():
    Session = sessionmaker()
    session = Session(bind = engine)
    lis = session.query(User).all()
    session.close()
    return lis

def bonus(username, bonus):
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(User).filter(User.username == username).first()
    curr.voices = curr.voices + int(bonus)
    session.commit()
    session.close()

def add_promo(name, act, gift):
    Session = sessionmaker()
    session = Session(bind = engine)
    new = Promos(name = name, activations = act, gift = gift)
    session.add(new)
    session.commit()
    session.close()

def all_promo():
    Session = sessionmaker()
    session = Session(bind = engine)
    allp = session.query(Promos).all()
    session.close()
    return allp
Base.metadata.create_all(engine)

