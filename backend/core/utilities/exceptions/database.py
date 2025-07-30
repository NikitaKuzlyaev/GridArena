class DatabaseException(Exception):
    """
    Базовый класс для исключений базы данных
    """


class EntityDoesNotExist(DatabaseException):
    """
    Throw an exception when the data does not exist in the database.
    """


class EntityAlreadyExists(DatabaseException):
    """
    Throw an exception when the data already exist in the database.
    """
