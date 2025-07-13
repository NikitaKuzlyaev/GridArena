from idlelib.rpc import request_queue
from typing import Sequence

import fastapi
from fastapi import Body
from fastapi import Depends, Request
from fastapi import Query, HTTPException
from starlette.responses import JSONResponse, Response

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.contest import ContestId, ContestCreateRequest, ContestUpdateRequest, ContestShortInfo
from core.services.interfaces.contest import IContestService
from core.services.providers.contest import get_contest_service

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
) -> JSONResponse:
    result: ContestId = (
        await contest_service.create_contest(
            user_id=user.id,
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})


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


@router.get(
    path="/",
    response_model=Sequence[ContestShortInfo],
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
    }
)
async def view_contests(
        user: User = Depends(get_user),
        contest_service: IContestService = Depends(get_contest_service),
) -> JSONResponse:
    result: Sequence[ContestShortInfo] = (
        await contest_service.get_user_contests(
            user_id=user.id,
        )
    )
    result = [i.model_dump() for i in result]

    return JSONResponse({'body': result})
