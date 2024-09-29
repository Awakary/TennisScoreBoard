import json
from parser import Parser

from exceptions import (IncorrectPlayerNameException, NotFullFormException,
                        SamePlayerNameException)
from pagination import Pagination
from render import Render
from service import Service
from session import create_new_match, get_finished_matches, get_player


class Handler:

    def __init__(self, method,  body, body_size):
        self.method = method
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
        matches = get_finished_matches()
        pagination = Pagination(queryset=matches, page_number=1)
        pagination_matches = pagination.get_objects_for_page()
        return Render().render_template(file_name='matches.html',
                                        pagination=pagination,
                                        render_objects=pagination_matches)

    def post(self):
        params = Parser.parse_params(self.body, self.body_size)
        matches = get_finished_matches(params=params)
        page_number = params.get('page_number', 1)
        last_page = params.get('last_page', None)
        back_page = params.get('back_page', None)
        pagination = Pagination(queryset=matches,
                                last_page=last_page,
                                back_page = back_page,
                                page_number=page_number)
        pagination_matches = pagination.get_objects_for_page()
        return Render().render_template(file_name='matches.html',
                                        pagination=pagination,
                                        render_objects=pagination_matches)


class NewMatchHandler(Handler):
    def get(self):
        return Render().render_template(file_name='new_match.html')

    def post(self):
        params = Parser.parse_params(self.body, self.body_size)
        player1 = params.get('player1', None)
        player2 = params.get('player2', None)
        if not (player1 and player2):
            raise NotFullFormException()
        if player1.isdigit() or player2.isdigit():
            raise IncorrectPlayerNameException()
        if player1 == player2:
            raise SamePlayerNameException()
        new_match = create_new_match(get_player(player1), get_player(player2))
        new_match.score = json.loads(new_match.score)
        return Render().render_template(file_name='match_score.html',
                                        render_objects=new_match)


class MatchScoreHandler(Handler):

    # def get(self):
    #     return Render().render_template(file_name='match_score.html',
    #                                     render_objects=match)
    def post(self):
        params = Parser.parse_params(self.body, self.body_size)
        match = Service().calculate_match_score(params)
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
        super().__init__(method=None, body=None, body_size=0)
        self.e = e
        self.path = path

    def get(self):
        setattr(self.e, 'path', self.path)
        return Render().render_template(file_name='error.html',
                                        render_objects=self.e)




