import fastapi
from fastapi import (
    Body,
    Depends,
)
from starlette.responses import JSONResponse

from backend.core.dependencies.authorization import get_user
from backend.core.models import User
from backend.core.schemas.submission import (
    SubmissionId,
    SubmissionCreateRequest,
)
from backend.core.services.interfaces.submission import ISubmissionService
from backend.core.services.providers.submission import get_submission_service
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from backend.core.utilities.exceptions.permission import PermissionDenied

router = fastapi.APIRouter(prefix="/submission", tags=["submission"])


@router.post(
    path="/",
    response_model=SubmissionId,
    status_code=201,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
        # todo: не логики проверки того, что пользователь может оправить посылку
        #  по уже решенной задаче или по задаче, где он превысил допустимое число попыток
    }
)
async def check_submission(
        params: SubmissionCreateRequest = Body(...),
        user: User = Depends(get_user),
        submission_service: ISubmissionService = Depends(get_submission_service),
) -> JSONResponse:
    """
    Отправляет ответ на выбранную задачу и инициирует проверку.

    Участник отправляет свой ответ на задачу, которую он выбрал ранее. Система проверяет ответ
    и возвращает результат (вердикт) СИНХРОННО.

    Args:
        params (SubmissionCreateRequest): Данные отправки:
            - selected_problem_id: ID выбранной задачи, к которой относится ответ
            - answer: текст ответа (до 32 символов)
        user (User): Авторизованный участник (определяется по JWT).
        submission_service (ISubmissionService): Сервис для обработки и проверки посылок.

    Returns:
        JSONResponse: Объект с ID созданной посылки в поле `body`

    Raises:
        Любые исключения обрабатываются на уровне сервиса или глобальным обработчиком.
        Типичные ошибки (неявно):
            - Если selected_problem_id не существует или не принадлежит пользователю
            - Если задача уже решена
            - Если превышено количество попыток
            - Если контест завершён

    Примечание:
        - Вердикт не возвращается в этом ответе — он доступен через опрос статуса.
        - Операция может повлиять на счёт участника (начисление/списание баллов) в зависимости от правил контеста.
    """

    result: SubmissionId = (
        await submission_service.check_submission(
            user_id=user.id,
            data=params,
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})
