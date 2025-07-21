from typing import Protocol

from core.schemas.selected_problem import SelectedProblemId


class ISelectedProblemService(Protocol):

    async def buy_selected_problem(
            self,
            user_id: int,
            selected_problem_id: int,
    ) -> SelectedProblemId:
        ...
