
from wsgiref.simple_server import make_server

from utils.exceptions import ExceptionWithMessage, UnknownErrorException
from handlers import ErrorHandler
from utils.response import Response
from router import Router


def app(environ, start_response):
    path = environ.get('PATH_INFO', None)
    query_string = environ.get('QUERY_STRING', None)
    method = environ.get('REQUEST_METHOD', None)
    body = environ.get('wsgi.input', None)
    body_size = environ.get('CONTENT_LENGTH', None)
    try:
        handler = Router(path=path).get_handler(method, body, body_size, query_string)
        response = Response(handler, path)
    except ExceptionWithMessage as e:
        response = Response(ErrorHandler(e, path).get())
    # except Exception as e:
    #     response = Response(ErrorHandler(UnknownErrorException(e), path).get())
    start_response(response.status, response.headers)
    return response.content


with make_server('', 8001, app) as httpd:
    print("Запуск сервера")
    httpd.serve_forever()
