from datetime import datetime
from typing import Sequence

# from core.dependencies.repository import get_repository, get_repository_manual
from core.models import Contest, ProblemCard
from core.models.permission import PermissionResourceType, PermissionActionType
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.problem_card import ProblemCardCRUDRepository
from core.repository.crud.quiz import QuizFieldCRUDRepository
from core.schemas.contest import ContestId, ContestShortInfo
from core.schemas.problem import ProblemId
from core.schemas.problem_card import ProblemCardId
from core.schemas.quiz_field import QuizFieldId

from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.problem_card import IProblemCardService
from core.services.interfaces.quiz import IQuizFieldService
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.loggers.log_decorator import log_calls


class ProblemCardService(IProblemCardService):
    def __init__(
            self,
            problem_card_repo: ProblemCardCRUDRepository,
    ):
        self.problem_card_repo = problem_card_repo

    @log_calls
    async def create_problem_card(
            self,
            problem_id: int,
            category_name: str,
            category_price: int,
            quiz_field_id: int,
            row: int,
            column: int,
    ) -> ProblemCardId:
        problem_card: ProblemCard = (
            await self.problem_card_repo.create_problem_card(
                problem_id=problem_id,
                category_name=category_name,
                category_price=category_price,
                quiz_field_id=quiz_field_id,
                row=row,
                column=column,
            )
        )
        res = ProblemCardId(problem_card_id=problem_card.id)

        return res

    @log_calls
    async def update_problem_card(
            self,
            problem_card_id: int,
            category_name: str,
            category_price: int,
    ) -> ProblemCardId:
        ...
