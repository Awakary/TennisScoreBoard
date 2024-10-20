import json
import os
import random
import sys

sys.path.append(os.getcwd())
from db.dao import DAO


def fill_db():
    if not DAO().get_finished_matches().count():
        players = ['Stan', 'Alex', 'Max', 'Luis', 'Roman', 'Nick', 'Ban', 'Ron', 'Ted', 'Martin', 'Leo',
                   'Stan', 'Alex', 'Max', 'Luis', 'Roman', 'Nick', 'Ban', 'Ron', 'Ted', 'Martin', 'Leo']
        for i in range(len(players) - 1):
            match = DAO().create_new_match(DAO().get_player(players[i]), DAO().get_player(players[i + 1]))
            match.score = json.loads(match.score)
            match.score['player1']['sets'], match.score['player2']['sets'] = 2, 1
            match.winner = match.player1
            match.score['player1']['completed_sets'], match.score['player2']['completed_sets'] = \
                ([random.randrange(0, 5), 6, 7], [6, random.randrange(0, 5), 5])
            DAO().update_match(match)

