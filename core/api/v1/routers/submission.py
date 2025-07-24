import fastapi
from fastapi import Body
from fastapi import Depends
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.submission import SubmissionId, SubmissionCreateRequest
from core.services.interfaces.submission import ISubmissionService
from core.services.providers.submission import get_submission_service
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper

router = fastapi.APIRouter(prefix="/submission", tags=["submission"])



@router.post(
    path="/",
    response_model=SubmissionId,
    status_code=201,
)
@async_http_exception_mapper(
    mapping={
    }
)
async def check_submission(
        params: SubmissionCreateRequest = Body(...),
        user: User = Depends(get_user),
        submission_service: ISubmissionService = Depends(get_submission_service),
) -> JSONResponse:

    result: SubmissionId = (
        await submission_service.check_submission(
            user_id=user.id,
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})
