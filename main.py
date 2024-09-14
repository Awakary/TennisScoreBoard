from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults

from controller import MatchHandler
from templates import *


def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]

    start_response(status, headers)

    # ret = [("%s: %s\n" % (key, value)).encode("utf-8")
    #        for key, value in environ.items()]
    # return ret
    if environ['PATH_INFO'] == '/new-match':
        if environ['REQUEST_METHOD'] == 'POST':
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            # ret = [("%s: %s\n" % (key, value)).encode("utf-8")
            #        for key, value in environ.items()]
            # return ret
            values = parse_qs(request_body)
            players = {k.decode(): v[0].decode() for k, v in values.items()}
            handler = MatchHandler(players)
            # handler.post()
            return ['1'.encode('utf-8')]

    with open('templates/new_match.html') as file:
        html = file.read()
    html_as_bytes = html.encode('utf-8')
    return [html_as_bytes]


with make_server('', 8000, simple_app) as httpd:
    print("Запуск сервера на порту 8000...")
    httpd.serve_forever()
