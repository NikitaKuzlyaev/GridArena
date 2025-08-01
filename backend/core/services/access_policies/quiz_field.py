from backend.core.models import QuizField
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.permission import PermissionPromise
from backend.core.services.access_policies.contest import ContestAccessPolicy
from backend.core.utilities.exceptions.database import EntityDoesNotExist


class QuizFieldAccessPolicy(ContestAccessPolicy):

    async def can_user_edit_quiz_field(
            self,
            uow: UnitOfWork,
            user_id: int,
            quiz_field_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:
        quiz_field: QuizField | None = (
            await uow.quiz_field_repo.get_quiz_field_by_id(quiz_field_id=quiz_field_id, ))
        if quiz_field is None:
            return self._raise_if(
                raise_if_none, f"QuizField with id={quiz_field_id} does not exists", EntityDoesNotExist)

        contest_id = quiz_field.contest_id
        await self.base_check(uow=uow, user_id=user_id, contest_id=contest_id, raise_if_none=raise_if_none)

        permission: PermissionPromise = (
            await self.can_user_manage_contest(
                uow=uow, user_id=user_id, contest_id=contest_id, raise_if_none=raise_if_none)
        )
        return permission

    async def can_contestant_view_quiz_field(
            self,
            uow: UnitOfWork,
            user_id: int,
            quiz_field_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:
        quiz_field: QuizField | None = (
            await uow.quiz_field_repo.get_quiz_field_by_id(quiz_field_id=quiz_field_id, ))
        if quiz_field is None:
            return self._raise_if(
                raise_if_none, f"QuizField with id={quiz_field_id} does not exists", EntityDoesNotExist)

        permission: PermissionPromise = (
            await self.can_user_view_contest(
                uow=uow, user_id=user_id, contest_id=quiz_field.contest_id, raise_if_none=raise_if_none)
        )
        return permission
