from datetime import datetime
from typing import Sequence, Tuple

from mako.testing.helpers import result_lines
from sqlalchemy import select, update, delete, and_, Row

from core.dependencies.repository import get_repository
from core.models import Contest, Permission, Problem, ProblemCard
from core.models.permission import PermissionResourceType, PermissionActionType
from core.repository.crud.base import BaseCRUDRepository
from core.schemas.contest import ContestId
from core.utilities.loggers.log_decorator import log_calls


class ProblemCardCRUDRepository(BaseCRUDRepository):

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
            update(
                ProblemCard
            )
            .where(
                ProblemCard.id == problem_card_id,
            )
            .values(
                category_name=category_name,
                category_price=category_price
            )
            .execution_options(
                synchronize_session="fetch"
            )
        )
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(
                ProblemCard
            ).where(
                ProblemCard.id == problem_card_id,
            )
        )
        return result.scalar_one_or_none()


problem_card_repo = get_repository(
    repo_type=ProblemCardCRUDRepository
)
