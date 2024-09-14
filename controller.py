from exceptions import (NotFullFormException, IncorrectPlayerNameException,
                        SamePlayerNameException)
from session import get_player, create_new_match


class MatchHandler:

    def __init__(self, players):
        self.player1 = players.get('player1', None)
        self.player2 = players.get('player2', None)

    def post(self):
        if not (self.player1 and self.player2):
            raise NotFullFormException()
        if self.player1.isdigit() or self.player2.isdigit():
            raise IncorrectPlayerNameException()
        if self.player1 == self.player2:
            raise SamePlayerNameException()
        player1_id = get_player(self.player1)
        player2_id = get_player(self.player2)
        new_match_uuid = create_new_match(player1_id, player2_id)



