from sqlalchemy import select, update

from core.dependencies.repository import get_repository
from core.models import QuizField
from core.repository.crud.base import BaseCRUDRepository


class QuizFieldCRUDRepository(BaseCRUDRepository):

    async def update_quiz_field(
            self,
            quiz_field_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizField | None:
        await self.async_session.execute(
            update(
                QuizField
            )
            .where(
                QuizField.id == quiz_field_id,
            )
            .values(
                number_of_rows=number_of_rows,
                number_of_columns=number_of_columns,
            )
            .execution_options(
                synchronize_session="fetch"
            )
        )
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(
                QuizField
            ).where(
                QuizField.id == quiz_field_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_quiz_field_by_id(
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

    async def get_quiz_field_by_contest_id(
            self,
            contest_id: int,
    ) -> QuizField | None:
        res = await self.async_session.execute(
            select(
                QuizField
            )
            .where(
                QuizField.contest_id == contest_id,
            )
        )
        return res.scalar_one_or_none()

    async def create_quiz_field(
            self,
            contest_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizField:
        quiz_field: QuizField = (
            QuizField(
                contest_id=contest_id,
                number_of_rows=number_of_rows,
                number_of_columns=number_of_columns,
            )
        )
        self.async_session.add(instance=quiz_field)
        await self.async_session.commit()
        await self.async_session.refresh(instance=quiz_field)
        return quiz_field


quiz_field_repo = get_repository(
    repo_type=QuizFieldCRUDRepository
)
