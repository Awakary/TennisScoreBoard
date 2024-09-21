import json

from session import get_match, get_player_name_by_id, update_match


class Service:

    def __init__(self):
        self.score = {1: 15, 2: 30, 3: 40, 4: 'AD'}

    def get_game_score(self):
        pass

    def get_set_score(self):
        pass

    def calculate_match_score(self, params):
        end = False
        match_uuid = params.get('uuid', None)
        if match_uuid:
            match = get_match(match_uuid)
            score_dict = json.loads(match.score)
            if not match.winner:
                if params.get('player1', None):
                    player_score = score_dict.get('player1')
                else:
                    player_score = score_dict.get('player2')
                if score_dict['player1']['points'] == 40 and score_dict['player2']['points'] == 40:
                    if params.get('player1', None):
                        score_dict['player1']['points'] = 'AD'
                    if params.get('player2', None):
                        score_dict['player2']['points'] = 'AD'
                elif score_dict['player1']['points'] == 'AD':
                    if params.get('player2', None):
                        score_dict['player1']['points'] = 40
                    if params.get('player1', None):
                        score_dict['player1']['points'] = 0
                        score_dict['player2']['points'] = 0
                        score_dict['player1']['games'] += 1
                elif score_dict['player2']['points'] == 'AD':
                    if params.get('player1', None):
                        score_dict['player2']['points'] = 40
                    if params.get('player2', None):
                        score_dict['player2']['points'] = 0
                        score_dict['player1']['points'] = 0
                        score_dict['player2']['games'] += 1

                else:
                    p = player_score['points']
                    g = player_score['games']
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
                            end = True

                    if params.get('player1', None):
                        score_dict['player1']['points'] = p
                        score_dict['player1']['games'] = g
                    elif params.get('player2', None):
                        score_dict['player2']['points'] = p
                        score_dict['player2']['games'] = g
                    if end:
                        score_dict['player1']['points'] = 0
                        score_dict['player2']['points'] = 0

                if (score_dict['player1']['games'] == 6
                        and score_dict['player2']['games'] <= 4):
                    score_dict['player1']['sets'] += 1
                    score_dict['player2']['games'] = 0
                    score_dict['player1']['games'] = 0
                elif (score_dict['player2']['games'] == 6
                      and score_dict['player1']['games'] <= 4):
                    score_dict['player2']['sets'] += 1
                    score_dict['player2']['games'] = 0
                    score_dict['player1']['games'] = 0
                elif (score_dict['player2']['games'] == 7              # тайбрейк
                        and score_dict['player1']['games'] == 6):
                    score_dict['player2']['sets'] += 1
                    score_dict['player2']['games'] = 0
                    score_dict['player1']['games'] = 0

                elif (score_dict['player2']['games'] == 6              # тайбрейк
                        and score_dict['player1']['games'] == 7):
                    score_dict['player1']['sets'] += 1
                    score_dict['player1']['games'] = 0
                    score_dict['player2']['games'] = 0
                match.score = score_dict
                if score_dict['player1']['sets'] == 2:  # победа 1 игрока
                    match.winner = match.player1
                elif score_dict['player2']['sets'] == 2:  # победа 2 игрока
                    match.winner = match.player2
                match = update_match(match)
                if match.winner:
                    setattr(match, 'winner_name', get_player_name_by_id(match.winner))
            else:
               pass
            setattr(match, 'player1_name', get_player_name_by_id(match.player1))
            setattr(match, 'player2_name', get_player_name_by_id(match.player2))
            match.score = json.loads(match.score)
            return match
