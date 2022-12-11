class IncorrectMoveError(Exception):
    pass


class IncorrectWordError(Exception):
    pass


class GameIsOverError(Exception):
    pass


class NotParsableResponseError(Exception):
    pass


class InternalConnectionError(Exception):
    pass


class NotEnoughLettersInRackError(Exception):
    pass