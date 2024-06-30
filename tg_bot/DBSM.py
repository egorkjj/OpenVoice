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
    username = Column(Text, nullable=True)
    chat_id = Column(Text, nullable=True, unique=True)
    is_subscriber = Column(Boolean, nullable=True)
    voices = Column(Integer, nullable=True)


def add_new(message: Message):
    Session = sessionmaker()
    session = Session(bind = engine)
    try:
        new = User(username = message.from_user.username, chat_id = message.chat.id, is_subscriber = False, voices = 10)
        session.add(new)
        session.commit()
    except:
        pass
    session.close()

def get_voices(chat_id):
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(User).filter(User.chat_id == chat_id).first()
    session.close()
    return curr.voices

def minus_voice(chat_id, voices):
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(User).filter(User.chat_id == chat_id).first()
    curr.voices = curr.voices - voices
    session.commit()
    session.close()
    

