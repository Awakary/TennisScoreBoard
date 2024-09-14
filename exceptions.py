
class NotFullFormException(Exception):
    def __init__(self):
        self.message = 'Количество имен игроков не равно 2'


class IncorrectPlayerNameException(Exception):
    def __init__(self):
        self.message = 'Имена игороков не могут состоять только из цифр'


class SamePlayerNameException(Exception):
    def __init__(self):
        self.message = 'Укажите разные имена игроков'



