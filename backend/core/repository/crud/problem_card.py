from typing import Sequence, Tuple

from sqlalchemy import select, update, Row

from backend.core.dependencies.repository import get_repository
from backend.core.models import Problem, ProblemCard
from backend.core.repository.crud.base import BaseCRUDRepository
from backend.core.utilities.loggers.log_decorator import log_calls


class ProblemCardCRUDRepository(BaseCRUDRepository):

    @log_calls
    async def create_problem_card_with_problem(
            self,
            quiz_field_id: int,
            row: int,
            column: int,
            category_name: str,
            category_price: int,
            statement: str,
            answer: str,
    ) -> Tuple[ProblemCard, Problem]:
        problem: Problem = (
            Problem(
                statement=statement,
                answer=answer,
            )
        )
        self.async_session.add(instance=problem)
        await self.async_session.flush()

        problem_card: ProblemCard = (
            ProblemCard(
                problem_id=problem.id,
                category_name=category_name,
                category_price=category_price,
                quiz_field_id=quiz_field_id,
                row=row,
                column=column,
            )
        )
        self.async_session.add(instance=problem_card)
        await self.async_session.commit()
        await self.async_session.refresh(instance=problem_card)
        return problem_card, problem

    @log_calls
    async def update_problem_card_with_problem(
            self,
            problem_card_id: int,
            problem_id: int,
            category_name: str,
            category_price: int,
            statement: str,
            answer: str,
    ) -> ProblemCard:
        await self.async_session.execute(
            update(ProblemCard)
            .where(ProblemCard.id == problem_card_id)
            .values(
                category_name=category_name,
                category_price=category_price,
            )
            .execution_options(synchronize_session="fetch")
        )
        await self.async_session.execute(
            update(Problem)
            .where(Problem.id == problem_id)
            .values(
                statement=statement,
                answer=answer
            )
            .execution_options(synchronize_session="fetch")
        )
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(ProblemCard)
            .where(ProblemCard.id == problem_card_id)
        )
        return result.scalar_one_or_none()

    @log_calls
    async def get_tuple_problem_card_with_problem_by_problem_card_id(
            self,
            problem_card_id: int,
    ) -> Tuple[ProblemCard, Problem] | None:
        res = await self.async_session.execute(
            select(
                ProblemCard,
                Problem
            )
            .outerjoin(
                Problem,
                Problem.id == ProblemCard.problem_id
            )
            .where(ProblemCard.id == problem_card_id)
        )
        res = res.one_or_none()
        return res

    @log_calls
    async def get_tuple_problem_cards_with_problem_by_quiz_field_id(
            self,
            quiz_field_id: int,
    ) -> Sequence[Row[Tuple[ProblemCard, Problem]]]:
        res = await self.async_session.execute(
            select(
                ProblemCard,
                Problem
            )
            .join(
                Problem,
                Problem.id == ProblemCard.problem_id
            )
            .where(ProblemCard.quiz_field_id == quiz_field_id)
        )
        res = res.all()
        return res

    @log_calls
    async def get_problem_card_by_id(
            self,
            problem_card_id: int,
    ) -> ProblemCard | None:
        res = await self.async_session.execute(
            select(ProblemCard)
            .where(ProblemCard.id == problem_card_id)
        )
        res = res.scalar_one_or_none()
        return res

    @log_calls
    async def get_problem_card_by_problem_id(
            self,
            problem_id: int,
    ) -> ProblemCard | None:
        res = await self.async_session.execute(
            select(ProblemCard)
            .where(ProblemCard.problem_id == problem_id)
        )
        res = res.scalar_one_or_none()
        return res

    @log_calls
    async def get_problem_cards_by_quiz_field_id(
            self,
            quiz_field_id: int,
    ) -> Sequence[ProblemCard]:
        res = await self.async_session.execute(
            select(ProblemCard)
            .where(ProblemCard.quiz_field_id == quiz_field_id)
        )
        res = res.scalars().all()
        return res

    @log_calls
    async def create_problem_card(
            self,
            problem_id: int,
            category_name: str,
            category_price: int,
            quiz_field_id: int,
            row: int,
            column: int,
    ) -> ProblemCard:
        problem_card: ProblemCard = (
            ProblemCard(
                problem_id=problem_id,
                category_name=category_name,
                category_price=category_price,
                quiz_field_id=quiz_field_id,
                row=row,
                column=column,
            )
        )
        self.async_session.add(instance=problem_card)
        await self.async_session.commit()
        await self.async_session.refresh(instance=problem_card)
        return problem_card

    @log_calls
    async def update_problem_card(
            self,
            problem_card_id: int,
            category_name: str,
            category_price: int,
    ) -> ProblemCard | None:
        await self.async_session.execute(
            update(ProblemCard)
            .where(ProblemCard.id == problem_card_id)
            .values(
                category_name=category_name,
                category_price=category_price
            )
            .execution_options(synchronize_session="fetch")
        )
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(ProblemCard)
            .where(ProblemCard.id == problem_card_id)
        )
        return result.scalar_one_or_none()


problem_card_repo = get_repository(
    repo_type=ProblemCardCRUDRepository
)
