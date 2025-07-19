import fastapi
from fastapi import Body
from fastapi import Depends
from fastapi import Query
from starlette.responses import JSONResponse

from core.dependencies.authorization import get_user
from core.models import User
from core.schemas.contest import ContestId, ContestCreateRequest, ContestUpdateRequest, ContestInfoForEditor, \
    ContestInfoForContestant, ArrayContestShortInfo
from core.schemas.contestant import ArrayContestantInfoForEditor, ContestantId, ContestantInCreate, \
    ContestantPreviewInfo
from core.services.interfaces.contest import IContestService
from core.services.interfaces.contestant import IContestantService
from core.services.interfaces.permission import IPermissionService
from core.services.providers.contest import get_contest_service
from core.services.providers.contestant import get_contestant_service
from core.services.providers.permission import get_permission_service
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from core.utilities.exceptions.permission import PermissionDenied

router = fastapi.APIRouter(prefix="/contestant", tags=["contestant"])


@router.post(
    path="/",
    response_model=ContestantId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def create_contestant(
        params: ContestantInCreate = Body(...),
        user: User = Depends(get_user),
        contestant_service: IContestantService = Depends(get_contestant_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> ContestantId:
    await permission_service.raise_if_not_all([
        lambda: permission_service.check_permission_for_edit_contest(user_id=user.id, contest_id=params.contest_id),
    ])

    result: ContestantId = (
        await contestant_service.create_contestant(
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return result


@router.get(
    path="/preview",
    response_model=ContestantPreviewInfo,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def preview_contestant_info(
        user: User = Depends(get_user),
        contestant_service: IContestantService = Depends(get_contestant_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> ContestantPreviewInfo:
    res: ContestantPreviewInfo = (
        await contestant_service.get_contestant_preview(
            user_id=user.id,
        )
    )
    res = res.model_dump()

    return res


@router.get(
    path="/",
    response_model=ArrayContestantInfoForEditor,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def view_contestants(
        contest_id: int = Query(...),
        user: User = Depends(get_user),
        contestant_service: IContestantService = Depends(get_contestant_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> ArrayContestantInfoForEditor:
    await permission_service.raise_if_not_all([
        lambda: permission_service.check_permission_for_edit_contest(user_id=user.id, contest_id=contest_id),
    ])

    result: ArrayContestantInfoForEditor = (
        await contestant_service.get_contestants_in_contest(
            user_id=user.id,
            contest_id=contest_id,
        )
    )
    result = result.model_dump()

    return result
