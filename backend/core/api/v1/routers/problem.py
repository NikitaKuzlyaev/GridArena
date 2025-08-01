import fastapi
from fastapi import (
    Body,
    Depends,
)
from starlette.responses import JSONResponse

from backend.core.dependencies.authorization import get_user
from backend.core.models import User
from backend.core.schemas.problem import (
    ProblemId,
    ProblemUpdateRequest,
)
from backend.core.services.interfaces.problem import IProblemService
from backend.core.services.providers.problem import get_problem_service
from backend.core.utilities.exceptions.handlers.http400 import async_http_exception_mapper

router = fastapi.APIRouter(prefix="/problem", tags=["problem"])


@router.patch(
    path="/",
    response_model=ProblemId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        NotImplementedError: (520, None),
    }
)
async def update_problem(
        params: ProblemUpdateRequest = Body(...),
        user: User = Depends(get_user),
        problem_service: IProblemService = Depends(get_problem_service),
) -> JSONResponse:
    # Этот эндпоинт не вызывается в текущей реализации

    raise NotImplementedError()
