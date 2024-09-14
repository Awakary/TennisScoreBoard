import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Player, Match
from settings import DB_URL

# создаем движок SqlAlchemy
engine = create_engine(DB_URL, echo=True)

# создаем класс сессии
Session = sessionmaker(autoflush=False, bind=engine)


def get_player(name):
    # создаем саму сессию базы данных
    with Session(autoflush=False, bind=engine) as db:
        player = db.query(Player).filter(Player.name == name).first()
        if player:
            return player.id
        else:
            # создаем объект Player для добавления в бд
            new_player = Player(name=name)
            db.add(new_player)             # добавляем в бд
            db.commit()                    # сохраняем изменения
            return new_player.id           # получаем установленный id


def create_new_match(player1_id, player2_id):
    with Session(autoflush=False, bind=engine) as db:
        new_match = Match(player1=player1_id, player2=player2_id, uuid=str(uuid.uuid4()))
        db.add(new_match)
        db.commit()
        return new_match.uuid
