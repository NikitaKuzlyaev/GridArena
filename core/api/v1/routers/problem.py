import fastapi
from fastapi import Body
from fastapi import Depends
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.problem import ProblemId, ProblemUpdateRequest
from core.services.interfaces.problem import IProblemService
from core.services.providers.problem import get_problem_service
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper

router = fastapi.APIRouter(prefix="/problem", tags=["problem"])


@router.patch(
    path="/",
    response_model=ProblemId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        EntityDoesNotExist: (404, None),
    }
)
async def update_problem(
        params: ProblemUpdateRequest = Body(...),
        user: User = Depends(get_user),
        problem_service: IProblemService = Depends(get_problem_service),
) -> JSONResponse:
    result: ProblemId = (
        await problem_service.update_problem(
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})
