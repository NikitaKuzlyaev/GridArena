class AuthException(Exception):
    """
    Базовый класс для исключений аутентификации
    """


class PasswordDoesNotMatch(AuthException):
    """
    Throw an exception when the account password does not match the entitiy's hashed password from the database.
    """


class TokenException(AuthException):
    """

    """


class InvalidToken(TokenException):
    """

    """


class ExpiredToken(TokenException):
    """

    """


class UndecodedToken(TokenException):
    """

    """


class UnauthorizedException(AuthException):
    """

    """
