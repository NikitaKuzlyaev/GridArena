from idlelib.rpc import request_queue
from typing import Sequence

import fastapi
from fastapi import Body
from fastapi import Depends, Request
from fastapi import Query, HTTPException
from starlette.responses import JSONResponse, Response

from core.dependencies.authorization import get_user
from core.models import User, QuizField
from core.schemas.contest import ContestId, ContestCreateRequest, ContestUpdateRequest, ContestShortInfo, \
    ContestInfoForEditor
from core.schemas.quiz_field import QuizFieldId, QuizFieldCreateRequest, QuizFieldUpdateRequest, QuizFieldInfoForEditor, \
    QuizFieldInfoForContestant
from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.quiz import IQuizFieldService
from core.services.providers.contest import get_contest_service
from core.services.providers.permission import get_permission_service
from core.services.providers.quiz import get_quiz_field_service

from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from core.utilities.exceptions.permission import PermissionDenied
from core.utilities.loggers.logger import logger

router = fastapi.APIRouter(prefix="/quiz-field", tags=["quiz-field"])




@router.patch(
    path="/",
    response_model=QuizFieldId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        EntityDoesNotExist: (404, None),
    }
)
async def update_quiz_field(
        params: QuizFieldUpdateRequest = Body(...),
        user: User = Depends(get_user),
        quiz_service: IQuizFieldService = Depends(get_quiz_field_service),
) -> QuizFieldId:
    # await permission_service.raise_if_not_all([
    #     lambda: permission_service.check_permission_for_edit_contest(user_id=user.id, contest_id=contest_id),
    # ])

    result: QuizFieldId = (
        await quiz_service.update_quiz_field(
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return result


@router.get(
    path="/info-editor",
    response_model=QuizFieldInfoForEditor,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def quiz_field_info_for_editor(
        contest_id: int = Query(...),
        user: User = Depends(get_user),
        quiz_field_service: IQuizFieldService = Depends(get_quiz_field_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> QuizFieldInfoForEditor:
    await permission_service.raise_if_not_all([
        lambda: permission_service.check_permission_for_edit_contest(user_id=user.id, contest_id=contest_id),
    ])

    result: QuizFieldInfoForEditor = (
        await quiz_field_service.quiz_field_info_for_editor(
            user_id=user.id,
            contest_id=contest_id,
        )
    )
    result = result.model_dump()

    return result


@router.get(
    path="/info-contestant",
    response_model=QuizFieldInfoForContestant,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def contest_info_for_contestant(
        contest_id=Query(...),
        user: User = Depends(get_user),
        quiz_field_service: IQuizFieldService = Depends(get_contest_service),
) -> JSONResponse:
    result: QuizFieldInfoForContestant = (
        await quiz_field_service.quiz_field_info_for_contestant(
            user_id=user.id,
            contest_id=contest_id,
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})
