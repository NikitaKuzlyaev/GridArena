from typing import (
    Type,
    TypeVar,
    Callable,
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies.session import get_async_session
from backend.core.repository.crud.base import BaseCRUDRepository
from backend.core.utilities.loggers.log_decorator import log_calls

T = TypeVar("T", bound=BaseCRUDRepository)


@log_calls
def get_repository(repo_type: Type[T]) -> Callable[[AsyncSession], T]:
    """
    Фабрика зависимости для внедрения репозиториев в ручки FastAPI.

    Принимает тип репозитория, унаследованный от BaseCRUDRepository, и возвращает функцию-зависимость,
    которая создаёт экземпляр репозитория с переданной асинхронной сессией.

    Args:
        repo_type (Type[T]): Класс репозитория, который необходимо внедрить. Должен быть подклассом BaseCRUDRepository.

    Returns:
        Callable[[AsyncSession], T]: Функция, совместимая с Depends, создающая экземпляр репозитория.
    """

    def _get_repo(
            async_session: AsyncSession = Depends(get_async_session),
    ) -> T:
        return repo_type(async_session=async_session)

    return _get_repo
