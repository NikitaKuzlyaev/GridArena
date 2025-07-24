from typing import cast, Protocol

from core.models import QuizField, User, Contestant, SelectedProblem, ProblemCard, Problem
from core.repository.crud.quiz import quiz_field_repo
from core.schemas.context import BaseQuizContext, UserContestantContext, SelectedProblemContext
from core.services.domain.submission import RepositoryUnit
from core.services.interfaces.context import IContextService
from core.utilities.exceptions.data_structures import NotEnoughParameters
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.exceptions.permission import PermissionDenied
from core.utilities.loggers.log_decorator import log_calls


class ContextService(IContextService):

    @log_calls
    async def get_selected_problem_context(
            self,
            repository_unit: RepositoryUnit,
            selected_problem_id: int,
    ) -> SelectedProblemContext:
        selected_problem: SelectedProblem | None = (
            await repository_unit.selected_problem_repo.get_selected_problem_by_id(
                selected_problem_id=selected_problem_id, ))
        if not selected_problem:
            raise EntityDoesNotExist("selected problem does not exist")

        problem_card: ProblemCard = (
            await repository_unit.problem_card_repo.get_problem_card_by_id(
                problem_card_id=selected_problem.problem_card_id, ))

        problem: Problem = (
            await repository_unit.problem_repo.get_problem_by_id(
                problem_id=problem_card.problem_id, ))

        user_contestant_context = await self.get_user_contestant_context(
            contestant_id=selected_problem.contestant_id, )

        res = SelectedProblemContext(
            **vars(user_contestant_context),
            selected_problem=selected_problem,
            problem_card=problem_card,
            problem=problem,
        )
        return res

    @log_calls
    async def get_user_contestant_context(
            self,
            repository_unit: RepositoryUnit,
            user_id: int | None = None,
            contestant_id: int | None = None,
    ) -> UserContestantContext:

        if user_id:
            user: User | None = (
                await repository_unit.user_repo.get_user_by_id(
                    user_id=user_id, ))
            if not user:
                raise EntityDoesNotExist("user not found")
            contestant: Contestant = (
                await repository_unit.contestant_repo.get_contestant_by_user_id(
                    user_id=user_id, ))

        elif contestant_id:
            contestant: Contestant | None = (
                await repository_unit.contestant_repo.get_contestant_by_id(
                    contestant_id=contestant_id, ))
            if not contestant:
                raise EntityDoesNotExist("contestant not found")
            user: User = (
                await repository_unit.user_repo.get_user_by_id(
                    user_id=contestant.user_id, ))

        else:
            raise NotEnoughParameters()

        return UserContestantContext(
            user=user,
            contestant=contestant,
        )
