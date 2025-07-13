from datetime import datetime
from typing import Protocol
from typing import Sequence

from core.models import Contest

from core.schemas.contest import ContestId, ContestCreateRequest, ContestShortInfo
from core.schemas.quiz_field import QuizFieldId


class IQuizService(Protocol):

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

    # async def update_quiz_field(
    #         self,
    #         quiz_field_id: int,
    #         number_of_rows: int,
    #         number_of_columns: int,
    # ) -> QuizFieldId:
    #     ...