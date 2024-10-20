class ExceptionWithMessage(Exception):
    def __init__(self):
        self.message = 'Ошибка'


class NotFullFormException(ExceptionWithMessage):
    def __init__(self):
        self.message = 'Количество имен игроков не равно 2'


class IncorrectPlayerNameException(ExceptionWithMessage):
    def __init__(self):
        self.message = 'Имена игороков не могут состоять только из цифр'


class SamePlayerNameException(ExceptionWithMessage):
    def __init__(self):
        self.message = 'Укажите разные имена игроков'


class NotFoundPathException(ExceptionWithMessage):
    def __init__(self):
        self.message = 'Нет такого url'


class NotParamUUID(ExceptionWithMessage):
    def __init__(self):
        self.message = 'Не указан uuid'


class NotFoundMatch(ExceptionWithMessage):
    def __init__(self):
        self.message = 'Нет матча с таким uuid'


class UnknownErrorException(ExceptionWithMessage):
    def __init__(self, e):
        self.message = e
