from handlers import (FonHandler, MainPageHandler, MatchesHandler,
                      MatchScoreHandler, NewMatchHandler, NormalizeHandler,
                      StylesHandler)
from utils.exceptions import NotFoundPathException


class Router:

    def __init__(self, path):
        self.path = path
        self.all_handlers = self.get_all_handlers()

    @staticmethod
    def get_all_handlers():
        all_handlers = {'/': MainPageHandler,
                        '/matches': MatchesHandler,
                        '/match_score': MatchScoreHandler,
                        '/new_match': NewMatchHandler,
                        '/static/normalize.css': NormalizeHandler,
                        '/static/styles.css': StylesHandler,
                        '/static/images/fon.jpg': FonHandler}
        return all_handlers

    def get_handler(self, method, body, body_size, query_string):

        handler = self.all_handlers.get(self.path, None)
        if handler:
            return handler(method, body, body_size, query_string).run_function()
        else:
            raise NotFoundPathException()

