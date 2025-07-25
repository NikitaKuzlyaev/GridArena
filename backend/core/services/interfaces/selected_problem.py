from typing import Protocol

from backend.core.schemas.selected_problem import SelectedProblemId, ArraySelectedProblemInfoForContestant


class ISelectedProblemService(Protocol):

    async def get_contestant_selected_problems(
            self,
            user_id: int,
    ) -> ArraySelectedProblemInfoForContestant:
        ...

    async def buy_selected_problem(
            self,
            user_id: int,
            selected_problem_id: int,
    ) -> SelectedProblemId:
        ...
