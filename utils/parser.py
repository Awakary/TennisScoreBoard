from urllib.parse import parse_qs


class Parser:

    @staticmethod
    def parse_params(body=None, body_size=None, query_string=None):
        if query_string:
            values = parse_qs(query_string)
        else:
            values = parse_qs(body.read(body_size).decode())
        params = {k: v[0] for k, v in values.items()}
        return params
