from typing import Protocol

from core.schemas.quiz_field import QuizFieldId, QuizFieldInfoForEditor, QuizFieldInfoForContestant


class IQuizFieldService(Protocol):

    async def quiz_field_info_for_contestant(
            self,
            user_id,
    ) -> QuizFieldInfoForContestant:
        ...

    async def quiz_field_info_for_editor(
            self,
            user_id,
            contest_id,
    ) -> QuizFieldInfoForEditor:
        ...

    async def create_quiz_field(
            self,
            contest_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizFieldId:
        ...

    async def update_quiz_field(
            self,
            quiz_field_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizFieldId:
        ...
