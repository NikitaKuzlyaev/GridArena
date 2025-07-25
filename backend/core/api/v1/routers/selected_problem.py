import fastapi
from fastapi import Body
from fastapi import Depends

from backend.core.dependencies.authorization import get_user
from backend.core.models import User
from backend.core.schemas.selected_problem import SelectedProblemId, SelectedProblemBuyRequest, \
    ArraySelectedProblemInfoForContestant
from backend.core.services.interfaces.contestant import IContestantService
from backend.core.services.interfaces.selected_problem import ISelectedProblemService
from backend.core.services.providers.contestant import get_contestant_service
from backend.core.services.providers.selected_problem import get_selected_problem_service
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from backend.core.utilities.exceptions.logic import PossibleLimitOverflow
from backend.core.utilities.exceptions.permission import PermissionDenied

router = fastapi.APIRouter(prefix="/selected-problem", tags=["selected-problem"])


@router.post(
    path="/buy",
    response_model=SelectedProblemId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
        PossibleLimitOverflow: (403, None),
    }
)
async def buy_problem(
        params: SelectedProblemBuyRequest = Body(...),
        user: User = Depends(get_user),
        contestant_service: IContestantService = Depends(get_contestant_service),
        selected_problem_service: ISelectedProblemService = Depends(get_selected_problem_service)
) -> SelectedProblemId:
    result: SelectedProblemId = (
        await selected_problem_service.buy_selected_problem(
            user_id=user.id,
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return result


@router.get(
    path="/my",
    response_model=ArraySelectedProblemInfoForContestant,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def get_contestant_selected_problems(
        user: User = Depends(get_user),
        selected_problem_service: ISelectedProblemService = Depends(get_selected_problem_service)
) -> ArraySelectedProblemInfoForContestant:
    result: ArraySelectedProblemInfoForContestant = (
        await selected_problem_service.get_contestant_selected_problems(
            user_id=user.id,
        )
    )
    result = result.model_dump()

    return result
