import json
import unittest

from db.models import Match
from service import Service


class TestService(unittest.TestCase):

    def setUp(self):
        score = {'player1': {'points': 0, 'games': 0, 'sets': 0},
                 'player2': {'points': 0, 'games': 0, 'sets': 0}}
        score = json.dumps(score)
        match = Match(player1=111,
                      player2=112,
                      uuid='2d45dc13-23da-45bf-a84a-7fb3609d8a4b',
                      score=score)
        params_player1 = {'player1': '111', 'uuid': '2d45dc13-23da-45bf-a84a-7fb3609d8a4b'}
        self.service_p1 = Service(match=match, params=params_player1)

        params_player2 = {'player2': '112', 'uuid': '2d45dc13-23da-45bf-a84a-7fb3609d8a4b'}
        self.service_p2 = Service(match=match, params=params_player2)

    def test_change_forty_to_AD(self):
        self.service_p1.score_dict = {'player1': {'points': 40, 'games': 0, 'sets': 0},
                           'player2': {'points': 40, 'games': 0, 'sets': 0}}
        self.service_p1.change_forty_to_AD()
        self.assertEqual(self.service_p1.score_dict['player1']['points'], 'AD')
        self.assertEqual(self.service_p1.score_dict['player2']['points'], 40)

    def test_change_AD_to_forty_1(self):
        self.service_p1.score_dict = {'player1': {'points': 'AD', 'games': 0, 'sets': 0},
                                      'player2': {'points': 40, 'games': 0, 'sets': 0}}
        self.service_p1.change_AD_to_forty_1()
        self.assertEqual(self.service_p1.score_dict['player1']['points'], 0)
        self.assertEqual(self.service_p1.score_dict['player2']['points'], 0)
        self.assertEqual(self.service_p1.score_dict['player1']['games'], 1)

    def test_change_AD_to_forty_2(self):
        self.service_p1.score_dict = {'player1': {'points': 40, 'games': 0, 'sets': 0},
                                      'player2': {'points': 'AD', 'games': 0, 'sets': 0}}
        self.service_p1.change_AD_to_forty_2()
        self.assertEqual(self.service_p1.score_dict['player2']['points'], 40)
        self.assertEqual(self.service_p1.score_dict['player1']['points'], 40)

    def test_process_game_from_15_to_30(self):
        self.service_p1.score_dict = {'player1': {'points': 15, 'games': 0, 'sets': 0},
                                      'player2': {'points': 15, 'games': 0, 'sets': 0}}
        self.service_p1.player_score = self.service_p1.get_player_score()
        self.service_p1.process_game()
        self.assertEqual(self.service_p1.score_dict['player1']['points'], 30)
        self.assertEqual(self.service_p1.score_dict['player2']['points'], 15)

    def test_process_game_from_30_to_40(self):
        self.service_p2.score_dict = {'player1': {'points': 15, 'games': 0, 'sets': 0},
                                      'player2': {'points': 30, 'games': 0, 'sets': 0}}
        self.service_p2.player_score = self.service_p2.get_player_score()
        self.service_p2.process_game()
        self.assertEqual(self.service_p2.score_dict['player2']['points'], 40)
        self.assertEqual(self.service_p2.score_dict['player1']['points'], 15)

    def test_process_game_win(self):
        self.service_p1.score_dict = {'player1': {'points': 40, 'games': 0, 'sets': 0},
                                      'player2': {'points': 0, 'games': 0, 'sets': 0}}
        self.service_p1.player_score = self.service_p1.get_player_score()
        self.service_p1.process_game()
        self.assertEqual(self.service_p1.score_dict['player1']['points'], 0)
        self.assertEqual(self.service_p1.score_dict['player1']['games'], 1)
        self.assertEqual(self.service_p1.score_dict['player2']['games'], 0)

    def test_determine_winner(self):
        self.service_p2.score_dict = {'player1': {'points': 0, 'games': 0, 'sets': 1},
                                      'player2': {'points': 0, 'games': 0, 'sets': 2}}
        self.service_p2.player_score = self.service_p2.get_player_score()
        self.service_p2.determine_winner()
        self.assertEqual(self.service_p2.match.winner, 112)

    def test_process_tai_brake(self):
        self.service_p2.score_dict = {'player1': {'points': 0, 'games': 6, 'sets': 1},
                                      'player2': {'points': 0, 'games': 6, 'sets': 1}}
        self.service_p2.player_score = self.service_p2.get_player_score()
        self.service_p2.process_tai_brake()
        self.assertEqual(self.service_p2.score_dict['player2']['points'], 1)
        self.assertEqual(self.service_p2.score_dict['player1']['points'], 0)
        self.assertEqual(self.service_p2.score_dict['player2']['games'], 6)
        self.assertEqual(self.service_p2.score_dict['player2']['games'], 6)

    def test_check_advantage(self):
        self.service_p2.score_dict = {'player1': {'points': 0, 'games': 3, 'sets': 0},
                                      'player2': {'points': 40, 'games': 6, 'sets': 0}}
        self.service_p2.player_score = self.service_p2.get_player_score()
        self.service_p2.check_advantage()
        self.assertEqual(self.service_p2.score_dict['player2']['sets'], 1)
        self.assertEqual(self.service_p2.score_dict['player1']['sets'], 0)
        self.assertEqual(self.service_p2.score_dict['player2']['games'], 0)
        self.assertEqual(self.service_p2.score_dict['player1']['games'], 0)

    def test_process_tennis_update_games(self):
        self.service_p2.score_dict = {'player1': {'points': 15, 'games': 0, 'sets': 0},
                                      'player2': {'points': 40, 'games': 0, 'sets': 0}}
        self.service_p2.player_score = self.service_p2.get_player_score()
        self.service_p2.process_tennis()
        self.assertEqual(self.service_p2.score_dict['player2']['games'], 1)
        self.assertEqual(self.service_p2.score_dict['player1']['games'], 0)
        self.assertEqual(self.service_p2.score_dict['player1']['points'], 0)
        self.assertEqual(self.service_p2.score_dict['player2']['points'], 0)

    def test_process_tennis_update_sets(self):
        self.service_p1.score_dict = {'player1': {'points': 40, 'games': 5, 'sets': 1},
                                      'player2': {'points': 15, 'games': 3, 'sets': 1}}
        self.service_p1.player_score = self.service_p1.get_player_score()
        self.service_p1.process_tennis()
        self.assertEqual(self.service_p1.score_dict['player1']['games'], 0)
        self.assertEqual(self.service_p1.score_dict['player2']['games'], 0)
        self.assertEqual(self.service_p1.score_dict['player1']['points'], 0)
        self.assertEqual(self.service_p1.score_dict['player2']['points'], 0)
        self.assertEqual(self.service_p1.score_dict['player1']['sets'], 2)
        self.assertEqual(self.service_p1.score_dict['player2']['sets'], 1)

