import json

from db.dao import DAO
from service import Service
from utils.exceptions import (IncorrectPlayerNameException, NotFoundMatch,
                              NotFullFormException, SamePlayerNameException, NotParamUUID)
from utils.pagination import Pagination
from utils.parser import Parser
from utils.render import Render


class Handler:

    def __init__(self, method,  body, body_size, query_string):
        self.method = method
        self.query_string = query_string
        self.body = body
        if body_size:
            self.body_size = int(body_size)

    def run_function(self):
        if self.method == 'GET':
            return self.get()
        if self.method == 'POST':
            return self.post()

    def get(self):
        pass

    def post(self):
        pass


class MainPageHandler(Handler):

    def get(self):
        return Render().render_template(file_name='index.html')


class MatchesHandler(Handler):

    def get(self):
        if self.query_string:
            query_params = Parser.parse_params(query_string=self.query_string)
            matches = DAO().get_finished_matches(params=query_params)
            page = query_params.get('page', 1)
            last_page = query_params.get('last_page', None)
            back_page = query_params.get('back_page', None)
            filtered_param = query_params.get('filter_by_player_name', None)
            pagination = Pagination(queryset=matches,
                                    last_page=last_page,
                                    back_page=back_page,
                                    page=page,
                                    filtered_param=filtered_param)
        else:
            matches = DAO().get_finished_matches()
            pagination = Pagination(queryset=matches, page=1)
        players = DAO().get_players()
        pagination_matches = pagination.get_objects_for_page()
        for match in pagination_matches:
            match.score = json.loads(match.score)
        return Render().render_template(file_name='matches.html',
                                        pagination=pagination,
                                        render_objects={'matches': pagination_matches,
                                                        'players': players})


class NewMatchHandler(Handler):
    def get(self):
        return Render().render_template(file_name='new_match.html')

    def post(self):
        params = Parser.parse_params(body=self.body, body_size=self.body_size)
        player1 = params.get('player1', None)
        player2 = params.get('player2', None)
        if not (player1 and player2):
            raise NotFullFormException()
        if player1.isdigit() or player2.isdigit():
            raise IncorrectPlayerNameException()
        if player1 == player2:
            raise SamePlayerNameException()
        new_match = DAO().create_new_match(DAO().get_player(player1), DAO().get_player(player2))
        new_match.score = json.loads(new_match.score)
        return Render().render_template(file_name='match_score.html',
                                        render_objects=new_match)


class MatchScoreHandler(Handler):

    def get(self):

        query_params = Parser.parse_params(query_string=self.query_string)
        match_uuid = query_params.get('uuid', None)
        if not match_uuid:
            raise NotParamUUID()
        try:
            match = DAO().get_match(match_uuid)
            match.score = json.loads(match.score)
        except AttributeError:
            raise NotFoundMatch()
        return Render().render_template(file_name='match_score.html',
                                        render_objects=match)

    def post(self):
        params = Parser.parse_params(body=self.body, body_size=self.body_size)
        match_uuid = params.get('uuid', None)
        match = DAO().get_match(match_uuid)
        try:
            match = Service(params=params, match=match).process_tennis()
            match = DAO().update_match(match)
            match.score = json.loads(match.score)
        except AttributeError:
            raise NotFoundMatch()
        return Render().render_template(file_name='match_score.html',
                                        render_objects=match)


class NormalizeHandler(Handler):
    def get(self):
        with open('static/normalize.css', "r") as f:
            resp_file = f.read()
            return resp_file


class StylesHandler(Handler):
    def get(self):
        with open('static/styles.css', "r") as f:
            resp_file = f.read()
            return resp_file


class FonHandler(Handler):
    def get(self):
        with open('static/images/fon.jpg', "rb") as f:
            resp_file = f.read()
            return resp_file


class ErrorHandler(Handler):

    def __init__(self, e, path):
        super().__init__(method=None, body=None, body_size=0, query_string=None)
        self.e = e
        self.path = path

    def get(self):
        setattr(self.e, 'path', self.path)
        return Render().render_template(file_name='error.html',
                                        render_objects=self.e)
