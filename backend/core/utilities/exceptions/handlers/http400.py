from functools import wraps
from typing import Type

from fastapi import HTTPException


def async_http_exception_mapper(
        mapping: dict[Type[Exception], tuple[int, str | None]] = None,
):
    if mapping is None:
        mapping = {}

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                for exc_type, (status, message) in mapping.items():
                    if isinstance(e, exc_type):
                        raise HTTPException(
                            status_code=status,
                            detail=message if message is not None else str(e),
                        )
                raise HTTPException(status_code=520, detail=str(e))

        return wrapper

    return decorator
