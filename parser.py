from urllib.parse import parse_qs


class Parser:

    @staticmethod
    def parse_params(body, body_size):
        values = parse_qs(body.read(body_size).decode())
        params = {k: v[0] for k, v in values.items()}
        return params
