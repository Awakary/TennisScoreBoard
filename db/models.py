from sqlalchemy import JSON, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship

from settings import DB_URL

engine = create_engine(DB_URL)


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "Player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True)


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


Base.metadata.create_all(bind=engine)
