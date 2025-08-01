from typing import (
    Optional,
    Callable,
    Awaitable,
)

from backend.core.models import (
    ProblemCard,
    QuizField,
    User,
    Contest,
)
from backend.core.models.permission import (
    PermissionResourceType,
    PermissionActionType,
    Permission,
)
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.permission import (
    PermissionId,
    PermissionPromise,
)
from backend.core.services.interfaces.permission import IPermissionService
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.exceptions.handlers.development import ObsoleteException
from backend.core.utilities.exceptions.permission import PermissionDenied


class PermissionService(IPermissionService):
    def __init__(
            self,
            uow: UnitOfWork,
    ):
        raise ObsoleteException('Сервис PermissionService упразднен')

    async def raise_if_not_all(
            self,
            permissions: list[Callable[[], Awaitable[Permission | None]]],
    ) -> None:
        raise ObsoleteException
        # for permission in permissions:
        #     result = await permission()
        #     if result is None:
        #         raise PermissionDenied('Permission denied')

    async def create_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: Optional[int] = None,
    ) -> PermissionId:
        raise ObsoleteException
        # async with self.uow:
        #     permission: Permission = (
        #         await self.uow.permission_repo.create_permission(
        #             user_id=user_id,
        #             resource_type=resource_type,
        #             resource_id=resource_id,
        #             permission_type=permission_type,
        #         )
        #     )
        #     res = PermissionId(
        #         permission_id=permission.id,
        #     )
        #     return res

    async def delete_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: Optional[int] = None,
    ) -> None:
        raise ObsoleteException

    async def check_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: Optional[int] = None,
    ) -> PermissionId | None:
        raise ObsoleteException
        # async with self.uow:
        #     permission: Permission = (
        #         await self.uow.permission_repo.check_permission(
        #             user_id=user_id,
        #             resource_type=resource_type,
        #             resource_id=resource_id if resource_id else user_id,
        #             permission_type=permission_type,
        #         )
        #     )
        #     if not permission:
        #         return None
        #
        #     res = PermissionId(
        #         permission_id=permission.id,
        #     )
        #     return res

    async def give_permission_for_admin_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId:
        raise ObsoleteException
        # res: PermissionId = (
        #     await self.create_permission(
        #         user_id=user_id,
        #         resource_type=PermissionResourceType.CONTEST.value,
        #         permission_type=PermissionActionType.ADMIN.value,
        #         resource_id=contest_id,
        #     )
        # )
        # return res

    async def check_permission_for_admin_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId | None:
        raise ObsoleteException
        # res: PermissionId = await self.check_permission(
        #     user_id=user_id,
        #     resource_type=PermissionResourceType.CONTEST.value,
        #     permission_type=PermissionActionType.ADMIN.value,
        #     resource_id=contest_id,
        # )
        # return res

    async def give_permission_for_edit_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId:
        raise ObsoleteException
        # res: PermissionId = (
        #     await self.create_permission(
        #         user_id=user_id,
        #         resource_type=PermissionResourceType.CONTEST.value,
        #         permission_type=PermissionActionType.EDIT.value,
        #         resource_id=contest_id,
        #     )
        # )
        # return res

    async def check_permission_for_edit_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId | None:
        raise ObsoleteException
        # res: PermissionId = (
        #     await self.check_permission(
        #         user_id=user_id,
        #         resource_type=PermissionResourceType.CONTEST.value,
        #         permission_type=PermissionActionType.EDIT.value,
        #         resource_id=contest_id,
        #     )
        # )
        # return res

    async def check_permission_for_edit_quiz_field(
            self,
            user_id: int,
            quiz_field_id: int,
    ) -> PermissionId | None:
        raise ObsoleteException
        # async with self.uow:
        #     quiz_field: QuizField = (
        #         await self.uow.quiz_field_repo.get_quiz_field_by_id(
        #             quiz_field_id=quiz_field_id,
        #         )
        #     )
        #     if not quiz_field:
        #         return None
        #
        #     res: PermissionId | None = (
        #         await self.check_permission_for_edit_contest(
        #             user_id=user_id,
        #             contest_id=quiz_field.contest_id,
        #         )
        #     )
        #     return res

    async def check_permission_for_edit_problem_card(
            self,
            user_id: int,
            problem_card_id: int,
    ) -> PermissionId | None:
        raise ObsoleteException
        # async with self.uow:
        #     problem_card: ProblemCard = (
        #         await self.uow.problem_card_repo.get_problem_card_by_id(
        #             problem_card_id=problem_card_id,
        #         )
        #     )
        #     if not problem_card:
        #         return None
        #
        #     res: PermissionId | None = (
        #         await self.check_permission_for_edit_quiz_field(
        #             user_id=user_id,
        #             quiz_field_id=problem_card.quiz_field_id,
        #         )
        #     )
        #     return res

    async def check_permission_for_edit_problem(
            self,
            user_id: int,
            problem_id: int,
    ) -> PermissionId | None:
        raise ObsoleteException
        # async with self.uow:
        #     problem_card: ProblemCard = (
        #         await self.uow.problem_card_repo.get_problem_card_by_problem_id(
        #             problem_id=problem_id,
        #         )
        #     )
        #     if not problem_card:
        #         return None
        #
        #     res: PermissionId | None = (
        #         await self.check_permission_for_edit_problem_card(
        #             user_id=user_id,
        #             problem_card_id=problem_card.id,
        #         )
        #     )
        #     return res

    async def check_permission_for_view_contest_standings(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionPromise | None:
        raise ObsoleteException
        # async with self.uow:
        #     user: User | None = (
        #         await self.uow.user_repo.get_user_by_id(
        #             user_id=user_id,
        #         )
        #     )
        #     if not user:
        #         raise EntityDoesNotExist("user not found")
        #
        #     contest: Contest | None = (
        #         await self.uow.contest_repo.get_contest_by_id(
        #             contest_id=contest_id,
        #         )
        #     )
        #     if not contest:
        #         raise EntityDoesNotExist("contest not found")
        #
        #     if user.domain_number == 0:
        #         permission: Permission | None = (
        #             await self.check_permission_for_edit_contest(
        #                 user_id=user_id,
        #                 contest_id=contest_id,
        #             )
        #         )
        #         if permission:
        #             return PermissionPromise()
        #         return None
        #     else:
        #         if user.domain_number == contest.id:
        #             return PermissionPromise()
        #         return None
