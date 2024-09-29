class Response:

    def __init__(self, handler, path=None):
        self.content = self.get_content(handler)
        self.path = path
        self.status = '200 OK'
        self.headers = [("Content-Type", self.content_type())]

    def content_type(self):
        path = self.path
        if path:
            if path.endswith(".css"):
                return "text/css"
        return "text/html"

    def get_content(self, handler):
        if isinstance(handler, bytes):
            return [handler]
        return [handler.encode('utf-8')]

