import json
import uuid

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker


from db.models import Match, Player
from settings import DB_URL


class DAO:

    def __init__(self):
        self.engine = create_engine(DB_URL, echo=True)                   # создаем движок SqlAlchemy
        self.session = sessionmaker(autoflush=False, bind=self.engine)   # создаем класс сессии

    def get_player(self, name):
        # создаем саму сессию базы данных
        with self.session(autoflush=False, bind=self.engine, expire_on_commit=False) as db:
            player = db.query(Player).filter(Player.name == name).first()
            if player:
                return player.id
            else:
                new_player = Player(name=name) # создаем объект Player для добавления в бд
                db.add(new_player)             # добавляем в бд
                db.commit()                    # сохраняем изменения
                return new_player.id           # получаем установленный id

    def get_player_name_by_id(self, id):
        with self.session(autoflush=False, bind=self.engine, expire_on_commit=False) as db:
            player = db.query(Player).get(id)
            return player.name

    def get_match(self, uuid):
        # создаем саму сессию базы данных
        with self.session(autoflush=False, bind=self.engine, expire_on_commit=False) as db:
            match = db.query(Match).filter(Match.uuid == uuid).first()
            if match:
                return match

    def get_players(self):
        with self.session(autoflush=False, bind=self.engine, expire_on_commit=False) as db:
            players = db.query(Player).all()
            return players

    def get_finished_matches(self, params=None):
        with self.session(autoflush=False, bind=self.engine, expire_on_commit=False) as db:
            matches = db.query(Match).filter(Match.winner != None).order_by(Match.id)
            if params:
                player_name = params.get('filter_by_player_name', None)
                if player_name:
                    matches = matches.filter(or_(Match.Player2.has(name=player_name),
                                                 Match.Player1.has(name=player_name)))
            return matches

    def create_new_match(self, player1_id, player2_id):
        with self.session(autoflush=False, bind=self.engine, expire_on_commit=False) as db:
            score = {'player1': {'points': 0, 'games': 0,  'sets': 0},
                     'player2': {'points': 0, 'games': 0, 'sets': 0}}
            score = json.dumps(score)
            new_match = Match(player1=player1_id,
                              player2=player2_id,
                              uuid=str(uuid.uuid4()),
                              score=score)
            db.add(new_match)
            db.commit()
            db.refresh(new_match)
            return new_match

    def update_match(self, match):
        with self.session(autoflush=False, bind=self.engine, expire_on_commit=False) as db:
            match_db = db.query(Match).get(match.id)
            match_db.score = json.dumps(match.score)
            match_db.winner = match.winner
            db.commit()
            return match_db

    def calculate_quantity_of_objects(self, queryset):
        return queryset.count()


