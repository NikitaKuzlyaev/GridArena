from datetime import datetime
from typing import Any

from backend.core.models import Contest, User, Contestant
from backend.core.models.permission import PermissionActionType, PermissionResourceType, Permission
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.permission import PermissionPromise
from backend.core.services.access_policies.base import AccessPolicy
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.exceptions.permission import PermissionDenied


class ContestAccessPolicy(AccessPolicy):

    def _raise_if(self, condition: bool, msg: str, ex_type: type[Exception] = PermissionDenied) -> None:
        if condition:
            raise ex_type(msg)

    async def can_user_view_contest(
            self,
            uow: UnitOfWork,
            user_id: int,
            contest_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:

        async with uow:
            user: User | None = await uow.user_repo.get_user_by_id(user_id=user_id)
            if user is None:
                # Пользователь не аутентифицирован
                return self._raise_if(
                    raise_if_none, f"User is not authenticated.")

            if user.domain_number == 0:
                # Пользователь принадлежит к домену сайта - может быть менеджером,
                # должен видеть только свои контесты (там, где он имеет права менеджера)
                permission: Permission | None = (
                    await uow.permission_repo.check_permission(
                        user_id=user_id,
                        resource_type=PermissionResourceType.CONTEST.value,
                        permission_type=PermissionActionType.EDIT.value,
                        resource_id=contest_id,
                    )
                )
                if permission is None:
                    return self._raise_if(
                        raise_if_none, "Permission denied: user is not the manager of this contest.")

            else:
                # Пользователь принадлежит к домену контеста - является участником,
                # должен видеть только свой контест
                if user.domain_number != contest_id:
                    return self._raise_if(
                        raise_if_none, f"User is not participating in this contest.")

                contest: Contest | None = (await uow.contest_repo.get_contest_by_id(contest_id=contest_id))
                if contest is None:
                    return self._raise_if(
                        raise_if_none, f"Contest does not exists.", EntityDoesNotExist)

                # Запрещаем доступ, если контест уже закончился
                current_time = datetime.now()
                if not contest.started_at < current_time < contest.closed_at:
                    return self._raise_if(
                        raise_if_none, f"Out of time: the contest has not started yet or has already ended.")

            return PermissionPromise()

    async def can_user_view_contest_submissions(
            self,
            uow: UnitOfWork,
            user_id: int,
            contest_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:

        # todo: временное решение

        res = await self.can_user_view_contest(uow, user_id, contest_id, raise_if_none)
        return res
