import fastapi
from fastapi import (
    Body,
    Depends,
    Query,
)

from backend.core.dependencies.authorization import get_user
from backend.core.models import User
from backend.core.schemas.contestant import (
    ArrayContestantInfoForEditor,
    ContestantId,
    ContestantInCreate,
    ContestantPreviewInfo,
    ContestantInfoInContest
)
from backend.core.schemas.contestant_log import ContestantLogPaginatedResponse
from backend.core.services.interfaces.contest import IContestService
from backend.core.services.interfaces.contestant import IContestantService
from backend.core.services.providers.contest import get_contest_service
from backend.core.services.providers.contestant import get_contestant_service
from backend.core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from backend.core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from backend.core.utilities.exceptions.permission import PermissionDenied

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
        EntityAlreadyExists: (409, None),
    }
)
async def create_contestant(
        params: ContestantInCreate = Body(...),
        user: User = Depends(get_user),
        contest_service: IContestService = Depends(get_contest_service),
) -> ContestantId:
    """
    Создаёт нового участника для указанного контеста.

    Пользователь должен иметь права на редактирование контеста (быть "менеджером" контеста).
    Эндпоинт используется менеджерами при регистрации новых участников на свое соревнование

    Args:
        params (ContestantInCreate): Данные для создания участника:
            - username: имя пользователя
            - password: пароль пользователя
            - name: имя пользователя, которое видно на странице соревнования
            - contest_id: ID контеста, для которого регистрируется участник
            - points: начальный баланс участника
        user (User): Текущий авторизованный пользователь (из JWT).
        contest_service (IContestService): Сервис для работы с контестом.

    Returns:
        ContestantId: Объект с полем `id` — идентификатором созданного участника.

    Raises:
        PermissionDenied: Если у пользователя нет прав на редактирование контеста.
        EntityDoesNotExist: Если контест с указанным `contest_id` не существует.
        EntityAlreadyExists: Если пользователь с указанным `username` уже существует в этом домене.
    """

    result: ContestantId = (
        await contest_service.create_contestant(
            user_id=user.id,
            contestant_data=params,
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
) -> ContestantPreviewInfo:
    """
    Получает превью о контесте и участии в нём текущего пользователя.

    Используется на фронтенде для отображения карточки участия перед входом в интерфейс контеста.

    Args:
        user (User): Авторизованный пользователь (определяется по JWT-токену).
        contestant_service (IContestantService): Сервис для получения данных участника.

    Returns:
        ContestantPreviewInfo: Модель с информацией:
            - contestant_id: ID участника
            - contestant_name: Полное имя участника
            - contest_id: ID контеста
            - contest_name: Название контеста
            - started_at: Время начала контеста (datetime)
            - closed_at: Время окончания контеста (datetime)
            - is_contest_open: True, если контест ещё активен (текущее время в диапазоне)

    Raises:
        PermissionDenied: Если у пользователя нет доступа к данным.
        EntityDoesNotExist: Если участник или связанный контест не найдены.
    """

    res: ContestantPreviewInfo = (
        await contestant_service.get_contestant_preview(
            user_id=user.id,
        )
    )
    res = res.model_dump()

    return res


@router.get(
    path="/info",
    response_model=ContestantInfoInContest,
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
) -> ContestantInfoInContest:
    """
    Получает информацию об участнике в контексте текущего контеста.

    Используется в интерфейсе контеста.

    Args:
        user (User): Авторизованный пользователь (определяется по JWT-токену).
        contestant_service (IContestantService): Сервис для получения данных участника.

    Returns:
        ContestantInfoInContest: Модель с информацией:
            - contestant_id: Уникальный ID участника
            - contestant_name: Полное имя участника
            - points: Количество баллов к текущему моменту
            - problems_current: Количество активных задач (тех, что куплены и решаются сейчас)
            - problems_max: Максимальное количество задач, которое можно иметь одновременно (из настроек контеста)

    Raises:
        PermissionDenied: Если у пользователя нет доступа к данным.
        EntityDoesNotExist: Если участник или его участие в контесте не найдено.
    """

    res: ContestantInfoInContest = (
        await contestant_service.get_contestant_info_in_contest(
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
) -> ArrayContestantInfoForEditor:
    """
    Получает список всех участников указанного контеста для редактирования.

    Требует прав на редактирование контеста. Возвращает список участников с их ID,
    именем и набранными баллами — в формате, пригодном для использования в интерфейсе администратора или редактора.

    Args:
        contest_id (int): ID контеста, участники которого запрашиваются.
        user (User): Авторизованный пользователь (определяется по JWT).
        contestant_service (IContestantService): Сервис для получения данных об участниках.

    Returns:
        ArrayContestantInfoForEditor: Объект, содержащий список участников в поле `body`,
        где каждый элемент — информация об участнике (ID, имя, баллы).

    Raises:
        PermissionDenied: Если у пользователя нет прав на редактирование контеста.
        EntityDoesNotExist: Если контест с указанным ID не существует.
    """

    result: ArrayContestantInfoForEditor = (
        await contestant_service.get_contestants_in_contest(
            user_id=user.id,
            contest_id=contest_id,
        )
    )
    result = result.model_dump()

    return result


@router.get(
    path="/my/logs",
    response_model=ContestantLogPaginatedResponse,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={

    }
)
async def contestant_logs_in_contest(
        user: User = Depends(get_user),
        contestant_service: IContestantService = Depends(get_contestant_service),
) -> ContestantLogPaginatedResponse:
    res: ContestantLogPaginatedResponse = (
        await contestant_service.get_contestant_logs_in_contest(
            user_id=user.id,
        )
    )
    res = res.model_dump()

    return res
