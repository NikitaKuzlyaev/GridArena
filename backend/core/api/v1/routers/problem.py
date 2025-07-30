import fastapi
from fastapi import (
    Body,
    Depends,
)
from starlette.responses import JSONResponse

from backend.core.dependencies.authorization import get_user
from backend.core.models import User
from backend.core.schemas.problem import ProblemId, ProblemUpdateRequest
from backend.core.services.interfaces.problem import IProblemService
from backend.core.services.providers.problem import get_problem_service
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.exceptions.handlers.http400 import async_http_exception_mapper

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
        user: User = Depends(get_user),  # todo: настроить проверку прав
        problem_service: IProblemService = Depends(get_problem_service),
) -> JSONResponse:
    """
    Обновляет текст условия и ответ задачи.

    Доступно только пользователям с правами на редактирование задачи (проверяется на уровне сервиса).
    Изменения применяются немедленно.

    Args:
        params (ProblemUpdateRequest): Новые данные задачи:
            - problem_id: ID задачи, которую необходимо обновить
            - statement: новое условие задачи (до 2048 символов)
            - answer: правильный ответ (до 32 символов)
        user (User): Авторизованный пользователь (определяется по JWT).
        problem_service (IProblemService): Сервис для обновления задачи.

    Returns:
        JSONResponse: Объект с обновлённым ID задачи в поле `body`

    Raises:
        EntityDoesNotExist: Если задача с указанным problem_id не существует (возвращает 404).

    Примечание:
        Изменение задачи НЕ влияет повлиять на уже отправленные посылки, если меняется ответ.
        Система должна корректно обрабатывать перепроверку при необходимости.
    """
    result: ProblemId = (
        await problem_service.update_problem(
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})
