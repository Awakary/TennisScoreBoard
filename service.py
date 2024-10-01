import json

from session import DAO


class Service:
    def __init__(self, params):
        self.params = params
        self.match = self.find_match()
        self.tai_brake = False
        self.end_game = False
        self.player1 = params.get('player1', None)
        self.player2 = params.get('player2', None)
        self.score_dict = json.loads(self.match.score)
        self.player_score = self.get_player_score()
        self.dict_points = {0: 0, 15: 15, 30: 30, 40: 40, 'AD': 'AD'}

    def process_tennis(self):
        if (self.score_dict['player1']['points'] == 40 and
                self.score_dict['player2']['points'] == 40):
            self.check_forty()
        elif self.score_dict['player1']['points'] == 'AD':
            self.check_AD_1()
        elif self.score_dict['player2']['points'] == 'AD':
            self.check_AD_2()
        elif (self.score_dict['player2']['games'] == 6  # тайбрейк
              and self.score_dict['player1']['games'] == 6):
            self.process_tai_brake()
        else:
            self.process_game()
        self.check_advantage()
        self.determine_winner()
        return self.update_match_in_db()

    def find_match(self):
        match_uuid = self.params.get('uuid', None)
        if match_uuid:
            return DAO().get_match(match_uuid)

    def get_player_score(self):

        if not self.match.winner:
            if self.player1:
                return self.score_dict.get('player1')
        return self.score_dict.get('player2')

    def process_game(self):
        p = self.player_score['points']
        g = self.player_score['games']
        match p:
            case 0:
                p = 15
            case 15:
                p = 30
            case 30:
                p = 40
            case 40:
                g += 1
                p = 0
                self.end_game = True
        if self.player1:
            self.score_dict['player1']['points'] = p
            self.score_dict['player1']['games'] = g
        elif self.player2:
            self.score_dict['player2']['points'] = p
            self.score_dict['player2']['games'] = g
        if self.end_game:
            self.score_dict['player1']['points'] = 0
            self.score_dict['player2']['points'] = 0

    def check_forty(self):
            if self.player1:
                self.score_dict['player1']['points'] = 'AD'
            if self.player2:
                self.score_dict['player2']['points'] = 'AD'

    def check_AD_1(self):
        if self.player2:
            print(2)
            self.score_dict['player1']['points'] = 40
        if self.player1:
            print(3)
            self.score_dict['player1']['points'] = 0
            self.score_dict['player2']['points'] = 0
            self.score_dict['player1']['games'] += 1

    def check_AD_2(self):

        if self.player1:
            print(4)
            self.score_dict['player2']['points'] = 40
        if self.player2:
            print(5)
            self.score_dict['player2']['points'] = 0
            self.score_dict['player1']['points'] = 0
            self.score_dict['player2']['games'] += 1

    def process_tai_brake(self):
        if self.player1:
            if self.score_dict['player1']['points'] != 6:
                self.score_dict['player1']['points'] += 1
            else:
                self.score_dict['player1']['sets'] += 1
                self.score_dict['player1']['points'] = 0
                self.score_dict['player2']['points'] = 0
                self.score_dict['player1']['games'] = 0
                self.score_dict['player2']['games'] = 0
        if self.player2:
            if self.score_dict['player2']['points'] != 6:
                self.score_dict['player2']['points'] += 1
            else:
                self.score_dict['player2']['sets'] += 1
                self.score_dict['player2']['points'] = 0
                self.score_dict['player1']['points'] = 0
                self.score_dict['player1']['games'] = 0
                self.score_dict['player2']['games'] = 0

    def check_advantage(self):
        if (self.score_dict['player1']['games'] == 6
                and self.score_dict['player2']['games'] <= 4
                and not self.tai_brake):
            self.score_dict['player1']['sets'] += 1
            self.score_dict['player2']['games'] = 0
            self.score_dict['player1']['games'] = 0
        elif (self.score_dict['player2']['games'] == 6
              and self.score_dict['player1']['games'] <= 4
              and not self.tai_brake):
            self.score_dict['player2']['sets'] += 1
            self.score_dict['player2']['games'] = 0
            self.score_dict['player1']['games'] = 0

    def determine_winner(self):
        self.match.score = self.score_dict
        if self.score_dict['player1']['sets'] == 2:  # победа 1 игрока
            self.match.winner = self.match.player1
        elif self.score_dict['player2']['sets'] == 2:  # победа 2 игрока
            self.match.winner = self.match.player2

    def update_match_in_db(self):
        match = DAO().update_match(self.match)
        match.score = json.loads(match.score)
        return match
