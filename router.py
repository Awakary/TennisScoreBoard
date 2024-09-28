from handlers import MatchesHandler, MatchScoreHandler, NewMatchHandler
from exceptions import NotFoundPathException


class Router:

    def __init__(self, path, method):
        self.path = path
        self.method = method
        self.all_handlers = self.get_all_handlers()

    def get_all_handlers(self):
        all_handlers = {'/matches': MatchesHandler,
                        '/match_score': MatchScoreHandler,
                        '/new_match': NewMatchHandler}
        return all_handlers

    def get_handler(self):
        handler = self.all_handlers.get(self.path, None)
        if handler:
            return handler
        else:
            raise NotFoundPathException()

