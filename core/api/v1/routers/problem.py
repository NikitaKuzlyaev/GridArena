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
from core.services.interfaces.contest import IContestService
from core.services.interfaces.problem import IProblemService
from core.services.interfaces.quiz import IQuizFieldService
from core.services.providers.contest import get_contest_service
from core.services.providers.problem import get_problem_service
from core.services.providers.quiz import get_quiz_service

from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from core.utilities.exceptions.permission import PermissionDenied
from core.utilities.loggers.logger import logger

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

# @router.get(
#     path="/",
#     response_model=Sequence[ContestShortInfo],
#     status_code=200,
# )
# @async_http_exception_mapper(
#     mapping={
#     }
# )
# async def view_contests(
#         user: User = Depends(get_user),
#         contest_service: IContestService = Depends(get_contest_service),
# ) -> JSONResponse:
#     result: Sequence[ContestShortInfo] = (
#         await contest_service.get_user_contests(
#             user_id=user.id,
#         )
#     )
#     result = [i.model_dump() for i in result]
#
#     return JSONResponse({'body': result})
