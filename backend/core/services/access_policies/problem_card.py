from backend.core.models import ProblemCard
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.permission import PermissionPromise
from backend.core.services.access_policies.quiz_field import QuizFieldAccessPolicy
from backend.core.utilities.exceptions.database import EntityDoesNotExist


class ProblemCardAccessPolicy(QuizFieldAccessPolicy):

    async def can_user_edit_problem_card(
            self,
            uow: UnitOfWork,
            user_id: int,
            problem_card_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:
        problem_card: ProblemCard | None = (
            await uow.problem_card_repo.get_problem_card_by_id(problem_card_id=problem_card_id)
        )
        if problem_card is None:
            return self._raise_if(
                raise_if_none, f"ProblemCard with id={problem_card_id} does not exists", EntityDoesNotExist)

        permission: PermissionPromise = (
            await self.can_user_edit_quiz_field(
                uow=uow, user_id=user_id, quiz_field_id=problem_card.quiz_field_id, raise_if_none=raise_if_none)
        )
        return permission

    async def can_contestant_view_problem_card(
            self,
            uow: UnitOfWork,
            user_id: int,
            problem_card_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:
        problem_card: ProblemCard | None = (
            await uow.problem_card_repo.get_problem_card_by_id(problem_card_id=problem_card_id)
        )
        if problem_card is None:
            return self._raise_if(
                raise_if_none, f"ProblemCard with id={problem_card_id} does not exists", EntityDoesNotExist)

        permission: PermissionPromise = (
            await self.can_contestant_view_quiz_field(
                uow=uow, user_id=user_id, quiz_field_id=problem_card.quiz_field_id, raise_if_none=raise_if_none)
        )
        return permission