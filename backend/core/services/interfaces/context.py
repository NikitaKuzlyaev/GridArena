from typing import Protocol


# from core.schemas.context import UserContestantContext, SelectedProblemContext
# from core.services.domain.submission import RepositoryUnit


class IContextService(Protocol):
    ...
    # async def get_user_contestant_context(
    #         self,
    #         repository_unit: RepositoryUnit,
    #         user_id: int | None = None,
    #         contestant_id: int | None = None,
    # ) -> UserContestantContext:
    #     ...
    #
    # async def get_selected_problem_context(
    #         self,
    #         repository_unit: RepositoryUnit,
    #         selected_problem_id: int,
    # ) -> SelectedProblemContext:
    #     ...
