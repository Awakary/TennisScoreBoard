import json


class Service:
    def __init__(self, params, match):
        self.params = params
        self.match = match
        self.tai_brake = False
        self.end_game = False
        self.player1 = params.get('player1', None)
        self.player2 = params.get('player2', None)
        self.score_dict = json.loads(self.match.score)
        self.player_score = self.get_player_score()

    def process_tennis(self):
        if (self.score_dict['player1']['points'] == 40 and
                self.score_dict['player2']['points'] == 40):
            self.change_forty_to_AD()
        elif self.score_dict['player1']['points'] == 'AD':
            self.change_AD_to_forty_1()
        elif self.score_dict['player2']['points'] == 'AD':
            self.change_AD_to_forty_2()
        elif (self.score_dict['player2']['games'] == 6  # тайбрейк
              and self.score_dict['player1']['games'] == 6):
            self.process_tai_brake()
        else:
            self.process_game()
        self.check_advantage()
        self.determine_winner()
        return self.match

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

    def change_forty_to_AD(self):
        if self.player1:
            self.score_dict['player1']['points'] = 'AD'
        if self.player2:
            self.score_dict['player2']['points'] = 'AD'

    def change_AD_to_forty_1(self):
        if self.player2:
            self.score_dict['player1']['points'] = 40
        if self.player1:
            self.score_dict['player1']['points'] = 0
            self.score_dict['player2']['points'] = 0
            self.score_dict['player1']['games'] += 1

    def change_AD_to_forty_2(self):
        if self.player1:
            self.score_dict['player2']['points'] = 40
        if self.player2:
            self.score_dict['player2']['points'] = 0
            self.score_dict['player1']['points'] = 0
            self.score_dict['player2']['games'] += 1

    def process_tai_brake(self):
        if self.player1:
            if self.score_dict['player1']['points'] != 6:
                self.score_dict['player1']['points'] += 1
            else:
                self.score_dict['player1']['sets'] += 1
                self.score_dict['player1']['completed_sets'].append(self.score_dict['player1']['games'])
                self.score_dict['player2']['completed_sets'].append(self.score_dict['player2']['games'])
                self.score_dict['player1']['points'] = 0
                self.score_dict['player2']['points'] = 0
                self.score_dict['player1']['games'] = 0
                self.score_dict['player2']['games'] = 0
        if self.player2:
            if self.score_dict['player2']['points'] != 6:
                self.score_dict['player2']['points'] += 1
            else:
                self.score_dict['player2']['sets'] += 1
                self.score_dict['player1']['completed_sets'].append(self.score_dict['player1']['games'])
                self.score_dict['player2']['completed_sets'].append(self.score_dict['player2']['games'])
                self.score_dict['player2']['points'] = 0
                self.score_dict['player1']['points'] = 0
                self.score_dict['player1']['games'] = 0
                self.score_dict['player2']['games'] = 0

    def check_advantage(self):
        if (self.score_dict['player1']['games'] == 6
                and self.score_dict['player2']['games'] <= 4
                and not self.tai_brake):
            self.score_dict['player1']['sets'] += 1
            self.score_dict['player1']['completed_sets'].append(self.score_dict['player1']['games'])
            self.score_dict['player2']['completed_sets'].append(self.score_dict['player2']['games'])
            self.score_dict['player2']['games'] = 0
            self.score_dict['player1']['games'] = 0
        elif (self.score_dict['player2']['games'] == 6
              and self.score_dict['player1']['games'] <= 4
              and not self.tai_brake):
            self.score_dict['player2']['sets'] += 1
            self.score_dict['player1']['completed_sets'].append(self.score_dict['player1']['games'])
            self.score_dict['player2']['completed_sets'].append(self.score_dict['player2']['games'])
            self.score_dict['player2']['games'] = 0
            self.score_dict['player1']['games'] = 0

    def determine_winner(self):
        self.match.score = self.score_dict
        if self.score_dict['player1']['sets'] == 2:  # победа 1 игрока
            self.match.winner = self.match.player1
        elif self.score_dict['player2']['sets'] == 2:  # победа 2 игрока
            self.match.winner = self.match.player2
