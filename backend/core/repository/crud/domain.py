from typing import Tuple

from sqlalchemy import (
    select,
)

from backend.core.models import Contestant, SelectedProblem, ProblemCard, Problem, User, QuizField, Contest
from backend.core.repository.crud.base import BaseCRUDRepository


class DomainCRUDRepository(BaseCRUDRepository):

    # async def get_problem_card_full_context(
    #         self,
    #         user_id: int,
    #         problem_card_id: int,
    # ) -> Tuple[User, Contestant, ProblemCard, SelectedProblem, QuizField, Contest] | None:
    #     stmt = (
    #         select(User, Contestant, ProblemCard, SelectedProblem, QuizField, Contest)
    #         .join(Contestant, Contestant.user_id == user_id)
    #         .join(Contest, Contest.id == User.domain_number)
    #         .join(QuizField, QuizField.contest_id == Contest.id)
    #         .join(ProblemCard, ProblemCard.quiz_field_id == QuizField.id)
    #         .join(SelectedProblem, SelectedProblem.problem_card_id == ProblemCard.id)
    #         .where(User.id == user_id)
    #         .where(ProblemCard.id == problem_card_id)
    #     )
    #     result = await self.async_session.execute(stmt)
    #     return result.one_or_none()

    async def get_selected_problem_full_context(
            self,
            user_id: int,
            selected_problem_id: int,
    ) -> Tuple[Contestant, SelectedProblem, ProblemCard, Problem] | None:
        stmt = (
            select(Contestant, SelectedProblem, ProblemCard, Problem)
            .join(SelectedProblem, SelectedProblem.contestant_id == Contestant.id)
            .join(ProblemCard, ProblemCard.id == SelectedProblem.problem_card_id)
            .join(Problem, Problem.id == ProblemCard.problem_id)
            .where(Contestant.user_id == user_id)
            .where(SelectedProblem.id == selected_problem_id)
        )
        result = await self.async_session.execute(stmt)
        return result.one_or_none()

    async def get_possible_reward_full_context(
            self,
            selected_problem_id: int,
    ) -> Tuple[SelectedProblem, ProblemCard, QuizField, Contest] | None:
        stmt = (
            select(SelectedProblem, ProblemCard, QuizField, Contest)
            .join(ProblemCard, ProblemCard.id == SelectedProblem.problem_card_id)
            .join(QuizField, QuizField.id == ProblemCard.quiz_field_id)
            .join(Contest, Contest.id == QuizField.contest_id)
            .where(SelectedProblem.id == selected_problem_id)
        )
        result = await self.async_session.execute(stmt)
        return result.one_or_none()


"""
Пример вызова

domain_repo = get_repository(
    repo_type=DomainCRUDRepository
)
"""
