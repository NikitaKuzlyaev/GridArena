from datetime import datetime, timezone
from typing import Tuple

from backend.core.models import (
    Contest,
    User,
)
from backend.core.models.permission import (
    PermissionActionType,
    PermissionResourceType,
    Permission,
)
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.permission import PermissionPromise
from backend.core.services.access_policies.base import AccessPolicy


class ContestAccessPolicy(AccessPolicy):

    async def base_check(
            self,
            uow: UnitOfWork,
            user_id: int,
            contest_id: int,
            raise_if_none: bool = True,
    ) -> Tuple[User, Contest] | None:
        async with uow:
            user_and_contest: Tuple[User, Contest] = await self._get_user_and_contest(uow, user_id, contest_id)
            user, contest = user_and_contest

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
                    return self._raise_if(raise_if_none, f"User is not participating in this contest.")

            return user, contest

    async def can_user_view_contest(
            self,
            uow: UnitOfWork,
            user_id: int,
            contest_id: int,
            raise_if_none: bool = True,
            **kwargs,
    ) -> PermissionPromise | None:

        async with uow:
            user_and_contest: Tuple[User, Contest] = await self.base_check(uow, user_id, contest_id, raise_if_none)
            user, contest = user_and_contest

            # Запрещаем доступ, если контест уже закончился
            current_time = datetime.now(timezone.utc)
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

    async def can_user_view_contest_standing(
            self,
            uow: UnitOfWork,
            user_id: int,
            contest_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:
        # todo: временное решение
        res = await self.can_user_view_contest(uow, user_id, contest_id, raise_if_none)
        return res

    async def can_user_create_contests(
            self,
            uow: UnitOfWork,
            user_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:
        user: User | None = await uow.user_repo.get_user_by_id(user_id=user_id)
        if user is None:  # Пользователь не аутентифицирован
            return self._raise_if(raise_if_none, f"User is not authenticated.")

        if user.domain_number != 0:
            return self._raise_if(raise_if_none, f"Yser of this domain cannot create contests.")

        return PermissionPromise()

    async def can_user_delete_contest(
            self,
            uow: UnitOfWork,
            user_id: int,
            contest_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:
        user_and_contest: Tuple[User, Contest] = await self.base_check(uow, user_id, contest_id, raise_if_none)
        user, contest = user_and_contest

        permission: Permission | None = (
            await uow.permission_repo.check_permission(
                user_id=user_id,
                resource_type=PermissionResourceType.CONTEST.value,
                permission_type=PermissionActionType.ADMIN.value,
                resource_id=contest_id,
            )
        )
        if permission is None:
            return self._raise_if(raise_if_none, "Permission denied: user is not the admin of this contest.")

        return PermissionPromise()

    async def can_user_manage_contest(
            self,
            uow: UnitOfWork,
            user_id: int,
            contest_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:
        user_and_contest: Tuple[User, Contest] = await self.base_check(uow, user_id, contest_id, raise_if_none)
        user, contest = user_and_contest

        permission: Permission | None = (
            await uow.permission_repo.check_permission(
                user_id=user_id,
                resource_type=PermissionResourceType.CONTEST.value,
                permission_type=PermissionActionType.EDIT.value,
                resource_id=contest_id,
            )
        )
        if permission is None:
            return self._raise_if(raise_if_none, "Permission denied: user is not the manager of this contest.")

        return PermissionPromise()
