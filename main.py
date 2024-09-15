from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults

from jinja2 import Environment, FileSystemLoader

from controller import MatchHandler
from service import Service


def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    if environ['PATH_INFO'] == '/match_score':
        if environ['REQUEST_METHOD'] == 'GET':
            return ['GET'.encode('utf-8')]
        if environ['REQUEST_METHOD'] == 'POST':
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            values = parse_qs(request_body)
            params = {k.decode(): v[0].decode() for k, v in values.items()}
            match = Service().calculate_match_score(params)
            template = env.get_template('match_score.html')
            html_as_bytes = template.render(match=match).encode('utf-8')
            return [html_as_bytes]

    if environ['PATH_INFO'] == '/new-match':
        if environ['REQUEST_METHOD'] == 'POST':
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            values = parse_qs(request_body)
            players = {k.decode(): v[0].decode() for k, v in values.items()}
            handler = MatchHandler(players)
            match = handler.get_match()
            template = env.get_template('match_score.html')
            html_as_bytes = template.render(match=match).encode('utf-8')
            return [html_as_bytes]
    template = env.get_template('new_match.html')
    html_as_bytes = template.render().encode('utf-8')
    return [html_as_bytes]


with make_server('', 8000, simple_app) as httpd:
    print("Запуск сервера на порту 8000...")
    httpd.serve_forever()
