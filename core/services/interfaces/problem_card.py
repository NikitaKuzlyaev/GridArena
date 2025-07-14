

from datetime import datetime
from typing import Protocol
from typing import Sequence

from core.models import Contest

from core.schemas.contest import ContestId, ContestCreateRequest, ContestShortInfo
from core.schemas.problem import ProblemId
from core.schemas.problem_card import ProblemCardId


class IProblemCardService(Protocol):

    # async def create_problem_card(
    #         self,
    #         statement: str,
    #         answer: str,
    # ) -> ProblemId:
    #     ...

    async def update_problem_card(
            self,
            problem_card_id: int,
            category_name: str,
            category_price: int,
    ) -> ProblemCardId:
        ...

