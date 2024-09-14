from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, ForeignKey, JSON, UUID
from sqlalchemy.engine.url import URL
from sqlalchemy import Column, Integer, String
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime

from settings import DB_URL

# строка подключения
engine = create_engine(DB_URL)

# engine = create_engine("postgresql+psycopg2://postgres:admin@localhost/tablo")


#создаем базовый класс для моделей
class Base(DeclarativeBase):
    pass


class Player(Base):

    __tablename__ = "Players"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True)


class Match(Base):

    __tablename__ = "Matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, unique=True)
    player1 = Column(Integer, ForeignKey('Players.id'))
    player2 = Column(Integer, ForeignKey('Players.id'))
    winner = Column(Integer, ForeignKey('Players.id'))
    score = Column(JSON)


# создаем таблицы
Base.metadata.create_all(bind=engine)

print("База данных и таблицы созданы")