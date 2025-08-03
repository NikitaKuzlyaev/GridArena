from functools import wraps
from typing import Type

from fastapi import HTTPException


def async_http_exception_mapper(
        mapping: dict[Type[Exception], tuple[int, str | None]] = None,
):
    """
    Фабрика декоратора для обработки исключений в асинхронных маршрутах FastAPI.

    Позволяет явно указать, какие исключения должны обрабатываться каким образом —
    с каким HTTP статусом и каким сообщением. Если возникла непредусмотренная ошибка,
    выбрасывается HTTP 520 (Unknown Error), сигнализируя о неучтённой ошибке.

    Args:
        mapping (dict[Type[Exception], tuple[int, str | None]]):
            Словарь, где ключ — тип исключения, а значение — кортеж из HTTP статуса
            и необязательного сообщения об ошибке. Если сообщение не указано (None),
            будет использовано строковое представление исключения.

    Returns:
        Callable: Декоратор, оборачивающий асинхронную функцию.
    """

    if mapping is None:
        mapping = {}

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            try:
                # Выполнение оборачиваемой асинхронной функции
                return await func(*args, **kwargs)

            except Exception as e:
                # Проверка типа исключения на соответствие ожидаемым
                for exc_type, (status, message) in mapping.items():
                    if isinstance(e, exc_type):
                        raise HTTPException(
                            status_code=status,
                            detail=message if message is not None else str(e),
                        )

                # Исключение не предусмотрено — ошибка в логике разработчика
                raise HTTPException(status_code=520, detail=str(e))

        return wrapper

    return decorator
