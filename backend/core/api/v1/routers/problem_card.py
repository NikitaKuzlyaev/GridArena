import fastapi
from fastapi import Body
from fastapi import Depends
from fastapi import Query
from starlette.responses import JSONResponse

from backend.core.dependencies.authorization import get_user
from backend.core.models import User
from backend.core.schemas.problem_card import ProblemCardId, ProblemCardUpdateRequest, ProblemCardInfoForEditor, \
    ProblemCardWithProblemUpdateRequest, ProblemCardWithProblemCreateRequest
from backend.core.services.interfaces.permission import IPermissionService
from backend.core.services.interfaces.problem_card import IProblemCardService
from backend.core.services.providers.permission import get_permission_service
from backend.core.services.providers.problem_card import get_problem_card_service
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from backend.core.utilities.exceptions.permission import PermissionDenied

router = fastapi.APIRouter(prefix="/problem-card", tags=["problem-card"])


@router.patch(
    path="/",
    response_model=ProblemCardId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def update_problem_card(
        params: ProblemCardUpdateRequest = Body(...),
        user: User = Depends(get_user),
        problem_card_service: IProblemCardService = Depends(get_problem_card_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> JSONResponse:
    await permission_service.raise_if_not_all([
        lambda: permission_service.check_permission_for_edit_problem_card(
            user_id=user.id, problem_card_id=params.problem_card_id),
    ])

    result: ProblemCardId = (
        await problem_card_service.update_problem_card(
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})


@router.get(
    path="/info-editor",
    response_model=ProblemCardInfoForEditor,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def problem_card_info_for_editor(
        problem_card_id: int = Query(...),
        user: User = Depends(get_user),
        problem_card_service: IProblemCardService = Depends(get_problem_card_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> ProblemCardInfoForEditor:
    await permission_service.raise_if_not_all([
        lambda: permission_service.check_permission_for_edit_problem_card(
            user_id=user.id, problem_card_id=problem_card_id),
    ])

    result: ProblemCardInfoForEditor = (
        await problem_card_service.problem_card_info_for_editor(
            user_id=user.id,
            problem_card_id=problem_card_id,
        )
    )
    result = result.model_dump()

    return result


@router.patch(
    path="/with-problem",
    response_model=ProblemCardId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def problem_card_info_for_editor(
        params: ProblemCardWithProblemUpdateRequest = Body(...),
        user: User = Depends(get_user),
        problem_card_service: IProblemCardService = Depends(get_problem_card_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> ProblemCardId:
    await permission_service.raise_if_not_all([
        lambda: permission_service.check_permission_for_edit_problem_card(
            user_id=user.id, problem_card_id=params.problem_card_id),
        lambda: permission_service.check_permission_for_edit_problem(
            user_id=user.id, problem_id=params.problem_id),
    ])

    result: ProblemCardId = (
        await problem_card_service.update_problem_card_with_problem(
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return result

@router.post(
    path="/with-problem",
    response_model=ProblemCardId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def problem_card_info_for_editor(
        params: ProblemCardWithProblemCreateRequest = Body(...),
        user: User = Depends(get_user),
        problem_card_service: IProblemCardService = Depends(get_problem_card_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> ProblemCardId:
    await permission_service.raise_if_not_all([
        lambda: permission_service.check_permission_for_edit_quiz_field(
            user_id=user.id, quiz_field_id=params.quiz_field_id),
    ])

    result: ProblemCardId = (
        await problem_card_service.create_problem_card_with_problem(
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return result
