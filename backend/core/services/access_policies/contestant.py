from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.permission import PermissionPromise
from backend.core.services.access_policies.contest import ContestAccessPolicy


class ContestantAccessPolicy(ContestAccessPolicy):

    async def can_user_view_other_contestant(
            self,
            uow: UnitOfWork,
            user_id: int,
            contest_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:
        async with uow:
            res = await self.can_user_manage_contest(
                uow=uow, user_id=user_id, contest_id=contest_id, raise_if_none=raise_if_none, )
            return res
