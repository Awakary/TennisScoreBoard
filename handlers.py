import json

from exceptions import (IncorrectPlayerNameException, NotFullFormException,
                        SamePlayerNameException)
from session import create_new_match, get_player


class MatchesHandler:

    def __init__(self, players):
        self.player1 = players.get('player1', None)
        self.player2 = players.get('player2', None)

    def get_match(self):
        if not (self.player1 and self.player2):
            raise NotFullFormException()
        if self.player1.isdigit() or self.player2.isdigit():
            raise IncorrectPlayerNameException()
        if self.player1 == self.player2:
            raise SamePlayerNameException()
        player1_id = get_player(self.player1)
        player2_id = get_player(self.player2)
        new_match = create_new_match(player1_id, player2_id)
        setattr(new_match, 'player1_name', self.player1)
        setattr(new_match, 'player2_name', self.player2)
        new_match.score = json.loads(new_match.score)
        return new_match


class NewMatchHandler:
    pass

class MatchScoreHandler:
    pass





