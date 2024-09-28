from datetime import datetime

from sqlalchemy import (JSON, UUID, Boolean, Column, DateTime, ForeignKey,
                        Integer, MetaData, String, Table, Text, create_engine)
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import DeclarativeBase, relationship

from settings import DB_URL

# строка подключения
engine = create_engine(DB_URL)

# engine = create_engine("postgresql+psycopg2://postgres:admin@localhost/tablo")


#создаем базовый класс для моделей
class Base(DeclarativeBase):
    pass


class Player(Base):

    __tablename__ = "Player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    # match = relationship("Match", back_populates="player")


class Match(Base):

    __tablename__ = "Match"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, unique=True)
    player1 = Column(Integer, ForeignKey('Player.id'))
    player2 = Column(Integer, ForeignKey('Player.id'))
    winner = Column(Integer, ForeignKey('Player.id'))
    score = Column(JSON)
    Player1 = relationship(
        "Player",
        foreign_keys=[player1],
        lazy='subquery'
    )
    Player2 = relationship(
        "Player",
        foreign_keys=[player2],
        lazy='subquery'
    )
    Winner = relationship(
        "Player",
        foreign_keys=[winner],
        lazy='subquery'
    )


# создаем таблицы
Base.metadata.create_all(bind=engine)

print("База данных и таблицы созданы")