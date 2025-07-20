from sqlalchemy import select, update

from core.dependencies.repository import get_repository
from core.models import QuizField
from core.repository.crud.base import BaseCRUDRepository


class SelectedProblemCRUDRepository(BaseCRUDRepository):

    async def get_selected_problem_by_id(
            self,
            quiz_field_id: int,
    ) -> QuizField | None:
        res = await self.async_session.execute(
            select(
                QuizField
            )
            .where(
                QuizField.id == quiz_field_id,
            )
        )
        return res.scalar_one_or_none()


selected_problem_repo = get_repository(
    repo_type=SelectedProblemCRUDRepository
)
