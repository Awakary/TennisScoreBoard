
from wsgiref.simple_server import make_server

from exceptions import ExceptionWithMessage, UnknownErrorException
from handlers import ErrorHandler
from response import Response
from router import Router


def simple_app(environ, start_response):
    path = environ.get('PATH_INFO', None)
    method = environ.get('REQUEST_METHOD', None)
    body = environ.get('wsgi.input', None)
    body_size = environ.get('CONTENT_LENGTH', None)
    try:
        handler = Router(path=path).get_handler(method, body, body_size)
        response = Response(handler, path)
    except ExceptionWithMessage as e:
        response = Response(ErrorHandler(e, path).get())
    except Exception as e:
        response = Response(ErrorHandler(UnknownErrorException(e), path).get())
    start_response(response.status, response.headers)
    return response.content


with make_server('', 8000, simple_app) as httpd:
    print("Запуск сервера")
    httpd.serve_forever()
