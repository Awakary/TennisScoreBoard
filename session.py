import json
import uuid

from sqlalchemy import create_engine, func, or_, table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from models import Match, Player
from settings import DB_URL

# создаем движок SqlAlchemy
engine = create_engine(DB_URL, echo=True)

# создаем класс сессии
Session = sessionmaker(autoflush=False, bind=engine)


def get_player(name):
    # создаем саму сессию базы данных
    with Session(autoflush=False, bind=engine, expire_on_commit=False) as db:
        player = db.query(Player).filter(Player.name == name).first()
        if player:
            return player.id
        else:
            # создаем объект Player для добавления в бд
            new_player = Player(name=name)
            db.add(new_player)             # добавляем в бд
            db.commit()                    # сохраняем изменения
            return new_player.id           # получаем установленный id


def get_player_name_by_id(id):
    with Session(autoflush=False, bind=engine, expire_on_commit=False) as db:
        player = db.query(Player).get(id)
        return player.name


def get_match(uuid):
    # создаем саму сессию базы данных
    with Session(autoflush=False, bind=engine, expire_on_commit=False) as db:
        match = db.query(Match).filter(Match.uuid == uuid).first()
        if match:
            return match


def get_finished_matches(params=None):
    with Session(autoflush=False, bind=engine, expire_on_commit=False) as db:
        matches = db.query(Match).filter(Match.winner != None).order_by(Match.id)
        if params:
            player_name = params.get('player_name', None)
            if player_name:
                matches = matches.filter(or_(Match.Player2.has(name=player_name), Match.Player1.has(name=player_name)))
            # page_number = params.get('page_number', None)
            # if page_number:
            #     matches = matches[int(page_number) * Pagination.page_size -
            #                       Pagination.page_size:int(page_number)*Pagination.page_size]
            #     print(int(page_number) * Pagination.page_size - Pagination.page_size)
            #     print(int(page_number)*Pagination.page_size)

        return matches


def create_new_match(player1_id, player2_id):
    with Session(autoflush=False, bind=engine, expire_on_commit=False) as db:
        score = {'player1': {'points': 0, 'games': 0, 'tie_break': 0, 'sets': 0},
                 'player2': {'points': 0, 'games': 0, 'tie_break': 0, 'sets': 0}}
        score = json.dumps(score)
        new_match = Match(player1=player1_id,
                          player2=player2_id,
                          uuid=str(uuid.uuid4()),
                          score=score)
        db.add(new_match)
        db.commit()
        db.refresh(new_match)
        return new_match


def update_match(match):
    with Session(autoflush=False, bind=engine, expire_on_commit=False) as db:
        match_db = db.query(Match).get(match.id)
        match_db.score = json.dumps(match.score)
        match_db.winner = match.winner
        db.commit()
        return match_db


def calculate_quantity_of_objects(queryset):
    return queryset.count()

