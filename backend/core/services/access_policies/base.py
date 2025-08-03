from typing import (
    Protocol,
    Tuple,
    Optional,
)

from backend.core.models import (
    Contest,
    User,
)
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.exceptions.permission import PermissionDenied


class AccessPolicy(Protocol):
    """
    Протокол для описания политики доступа.

    Классы, реализующие этот протокол, должны определять правила доступа
    к определённым ресурсам или действиям на основе предоставленных данных.

    Этот класс подразумевает наследование от него низкоуровневых классов с
    правилами проверки доступа для каждого домена.

    Например, ContestAccessPolicy(AccessPolicy) - класс, определяющий методы проверки доступа
    пользователя к ресурсам, предоставляемых реализацией IContestService (например, ContestService)
    """

    @staticmethod
    def _raise_if(condition: bool, msg: str, ex_type: type[Exception] = PermissionDenied) -> None:
        if condition:
            raise ex_type(msg)

    async def _get_user_and_contest(
            self,
            uow: UnitOfWork,
            user_id: int,
            contest_id: Optional[int] = None,
            raise_if_none: bool = True,
    ) -> Tuple[User, Contest] | None:
        async with uow:
            user: User | None = await uow.user_repo.get_user_by_id(user_id=user_id)
            if user is None:  # Пользователь не аутентифицирован
                return self._raise_if(raise_if_none, f"User is not authenticated.")

            contest_id = contest_id or user.domain_number
            contest: Contest | None = (await uow.contest_repo.get_contest_by_id(contest_id=contest_id))
            if contest is None:  # Контест не существует
                return self._raise_if(raise_if_none, f"Contest does not exists.", EntityDoesNotExist)

            return user, contest
