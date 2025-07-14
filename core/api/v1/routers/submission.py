from idlelib.rpc import request_queue
from typing import Sequence

import fastapi
from fastapi import Body
from fastapi import Depends, Request
from fastapi import Query, HTTPException
from starlette.responses import JSONResponse, Response

from core.dependencies.authorization import get_user
from core.models import User, QuizField
from core.schemas.contest import ContestId, ContestCreateRequest, ContestUpdateRequest, ContestShortInfo
from core.schemas.problem import ProblemId, ProblemUpdateRequest
from core.schemas.quiz_field import QuizFieldId, QuizFieldCreateRequest, QuizFieldUpdateRequest
from core.schemas.submission import SubmissionId, SubmissionCreateRequest
from core.services.interfaces.contest import IContestService
from core.services.interfaces.problem import IProblemService
from core.services.interfaces.quiz import IQuizFieldService
from core.services.interfaces.submission import ISubmissionService
from core.services.providers.contest import get_contest_service
from core.services.providers.problem import get_problem_service
from core.services.providers.quiz import get_quiz_field_service
from core.services.providers.submission import get_submission_service

from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from core.utilities.exceptions.permission import PermissionDenied
from core.utilities.loggers.logger import logger

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
async def create_submission(
        params: SubmissionCreateRequest = Body(...),
        user: User = Depends(get_user),
        submission_service: ISubmissionService = Depends(get_submission_service),
) -> JSONResponse:
    result: SubmissionId = (
        await submission_service.create_submission(
            user_id=user.id,
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})
