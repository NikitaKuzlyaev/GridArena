class PermissionException(Exception):
    """
    Базовый класс для исключений, связанных с политикой доступа к ресурсам приложения
    """


class PermissionDenied(Exception):
    """
    Запрашиваемый ресурс недоступен
    """
