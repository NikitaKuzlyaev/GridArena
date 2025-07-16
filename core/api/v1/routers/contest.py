from idlelib.rpc import request_queue
from typing import Sequence

import fastapi
from fastapi import Body
from fastapi import Depends, Request
from fastapi import Query, HTTPException
from starlette.responses import JSONResponse, Response

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.contest import ContestId, ContestCreateRequest, ContestUpdateRequest, ContestShortInfo, \
    ContestInfoForEditor, ContestInfoForContestant, ArrayContestShortInfo
from core.schemas.problem import ProblemId
from core.schemas.problem_card import ProblemCardId
from core.schemas.quiz_field import QuizFieldId
from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.problem import IProblemService
from core.services.interfaces.problem_card import IProblemCardService
from core.services.interfaces.quiz import IQuizFieldService
from core.services.providers.contest import get_contest_service
from core.services.providers.permission import get_permission_service
from core.services.providers.problem import get_problem_service
from core.services.providers.problem_card import get_problem_card_service
from core.services.providers.quiz import get_quiz_field_service

from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from core.utilities.exceptions.permission import PermissionDenied
from core.utilities.loggers.logger import logger

router = fastapi.APIRouter(prefix="/contest", tags=["contest"])


@router.post(
    path="/",
    response_model=ContestId,
    status_code=201,
)
@async_http_exception_mapper(
    mapping={
    }
)
async def create_contest(
        params: ContestCreateRequest = Body(...),
        user: User = Depends(get_user),
        contest_service: IContestService = Depends(get_contest_service),
        quiz_field_service: IQuizFieldService = Depends(get_quiz_field_service),
        problem_service: IProblemService = Depends(get_problem_service),
        problem_card_service: IProblemCardService = Depends(get_problem_card_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> ContestId:
    res: ContestId = (
        await contest_service.create_full_contest(
            user_id=user.id,
            **params.model_dump(),
        )
    )

    await permission_service.give_permission_for_admin_contest(
        user_id=user.id, contest_id=res.contest_id,
    )
    await permission_service.give_permission_for_edit_contest(
        user_id=user.id, contest_id=res.contest_id,
    )

    return res


@router.patch(
    path="/",
    response_model=ContestId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        EntityDoesNotExist: (404, None),
    }
)
async def update_contest(
        params: ContestUpdateRequest = Body(...),
        user: User = Depends(get_user),
        contest_service: IContestService = Depends(get_contest_service),
) -> JSONResponse:
    result: ContestId = (
        await contest_service.update_contest(
            user_id=user.id,
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})


@router.delete(
    path="/",
    status_code=204,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
    }
)
async def delete_contest(
        contest_id: int = Query(...),
        user: User = Depends(get_user),
        contest_service: IContestService = Depends(get_contest_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> None:
    await permission_service.raise_if_not_all([
        lambda: permission_service.check_permission_for_admin_contest(user_id=user.id, contest_id=contest_id),
    ])

    await contest_service.delete_contest(
        user_id=user.id,
        contest_id=contest_id,
    )

    return None


@router.get(
    path="/",
    response_model=ArrayContestShortInfo,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
    }
)
async def view_contests(
        user: User = Depends(get_user),
        contest_service: IContestService = Depends(get_contest_service),
) -> ArrayContestShortInfo:
    result: ArrayContestShortInfo = (
        await contest_service.get_user_contests(
            user_id=user.id,
        )
    )
    result = result.model_dump()
    return result


@router.get(
    path="/info-editor",
    response_model=ContestInfoForEditor,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def contest_info_for_editor(
        contest_id: int = Query(...),
        user: User = Depends(get_user),
        contest_service: IContestService = Depends(get_contest_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> ContestInfoForEditor:
    await permission_service.raise_if_not_all([
        lambda: permission_service.check_permission_for_edit_contest(user_id=user.id, contest_id=contest_id),
    ])

    result: ContestInfoForEditor = (
        await contest_service.contest_info_for_editor(
            user_id=user.id,
            contest_id=contest_id,
        )
    )
    result = result.model_dump()

    return result


@router.get(
    path="/info-contestant",
    response_model=ContestInfoForContestant,
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
        contest_service: IContestService = Depends(get_contest_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    result: ContestInfoForContestant = (
        await contest_service.contest_info_for_contestant(
            user_id=user.id,
            contest_id=contest_id,
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})
