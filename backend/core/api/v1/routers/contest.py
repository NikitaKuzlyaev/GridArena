import fastapi
from fastapi import (
    Body,
    Depends,
    Query,
)
from starlette.responses import JSONResponse

from backend.core.dependencies.authorization import get_user
from backend.core.models import User
from backend.core.schemas.contest import (
    ContestId,
    ContestCreateRequest,
    ContestUpdateRequest,
    ContestInfoForEditor,
    ContestInfoForContestant,
    ArrayContestShortInfo,
    ContestStandings,
    ContestSubmissions
)
from backend.core.services.interfaces.contest import IContestService
from backend.core.services.providers.contest import get_contest_service
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from backend.core.utilities.exceptions.permission import PermissionDenied

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
) -> ContestId:
    """
    Создаёт новый контест с заданными параметрами.

    После создания контеста инициализируется полный набор прав для создателя:
    - Право администрировать контест
    - Право редактировать контест

    Args:
        params (ContestCreateRequest): Параметры создания контеста:
            - name: название (до 256 символов)
            - started_at: дата и время начала контеста
            - closed_at: дата и время окончания
            - start_points: стартовый баланс участников (0–10000)
            - number_of_slots_for_problems: количество задач, которые участник может держать одновременно (1–5)
        user (User): Авторизованный пользователь, создающий контест (определяется по JWT).
        contest_service (IContestService): Сервис для создания контеста.
        permission_service (IPermissionService): Сервис для выдачи прав на управление контестом.

    Returns:
        ContestId: Объект с единственным полем:
            - contest_id: уникальный идентификатор созданного контеста

    Raises:
        ValueError:
            - Если closed_at < started_at (проверяется через model_validator)

    Валидация:
        - Поля проходят валидацию по типу, длине, диапазону (Field)
        - Даты проверяются на корректность порядка (через @model_validator)
    """

    res: ContestId = (
        await contest_service.create_full_contest(
            user_id=user.id,
            **params.model_dump(),
        )
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
    """
    Обновляет параметры существующего контеста.

    Позволяет изменить основные настройки контеста: название, даты, баллы, правила и другие параметры.
    Доступно только пользователям с правами на редактирование контеста.

    Args:
        params (ContestUpdateRequest): Новые данные для контеста:
            - contest_id: ID контеста, который нужно обновить
            - name: новое название (до 256 символов)
            - started_at, closed_at: новые даты начала и окончания
            - start_points: стартовый баланс участников (0–10000)
            - number_of_slots_for_problems: количество задач, которые можно держать одновременно (1–5)
            - rule_type: тип правил контеста
            - flag_user_can_have_negative_points: разрешены ли отрицательные баллы у участников
        user (User): Авторизованный пользователь (определяется по JWT).
        contest_service (IContestService): Сервис для обновления контеста.

    Returns:
        JSONResponse: Объект с обновлённым contest_id в поле `body`:

    Raises:
        EntityDoesNotExist: Если контест с указанным contest_id не существует (возвращает 404).
        ValueError: Если closed_at < started_at (проверяется через model_validator).

    Валидация:
        - Все поля проходят строгую валидацию (диапазоны, длина)
        - Даты проверяются на корректность порядка
    """

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
) -> None:
    """
    Удаляет контест по его ID.

    Операция доступна только пользователям с правами администратора контеста.
    При удалении контеста удаляются все связанные с ним данные (участники, задачи, попытки и т.д.).

    Args:
        contest_id (int): ID контеста, который необходимо удалить (передаётся в query-параметре).
        user (User): Авторизованный пользователь (определяется по JWT).
        contest_service (IContestService): Сервис для удаления контеста.
        permission_service (IPermissionService): Сервис для проверки прав администратора.

    Returns:
        None: Успешный ответ без тела (204 No Content).

    Raises:
        PermissionDenied: Если у пользователя нет прав администратора на указанный контест (возвращает 403).
        EntityDoesNotExist: Может быть выброшено внутри contest_service, если контест не найден (обрабатывается глобально).

    Status Code:
        204 No Content — контест успешно удалён, тело ответа пустое

    Примечание:
        Удаление — необратимая операция. Все данные контеста будут безвозвратно удалены.
    """

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
    """
    Получает список всех контестов, в которых пользователь является администратором.

    Возвращает краткую информацию о каждом контесте: ID, название, даты начала и окончания.

    Args:
        user (User): Авторизованный пользователь (определяется по JWT).
        contest_service (IContestService): Сервис для получения списка контестов пользователя.

    Returns:
        ArrayContestShortInfo: Объект с полем `body`, содержащим список контестов:
            - contest_id: уникальный идентификатор контеста
            - name: название контеста
            - started_at: дата и время начала
            - closed_at: дата и время окончания

    Raises:
        todo: add later
    """

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
) -> ContestInfoForEditor:
    """
    Получает полную информацию о контесте для редактора (администратора/организатора).

    Доступно только пользователям с правами на редактирование контеста.
    Возвращает все редактируемые параметры контеста, включая правила и настройки баллов.

    Args:
        contest_id (int): ID контеста, информация о котором запрашивается (передаётся в query).
        user (User): Авторизованный пользователь (определяется по JWT).
        contest_service (IContestService): Сервис для получения данных контеста.
        permission_service (IPermissionService): Сервис для проверки прав на редактирование.

    Returns:
        ContestInfoForEditor: Объект с полной информацией о контесте:
            - contest_id: ID контеста
            - name: название
            - start_points: стартовый баланс участников
            - number_of_slots_for_problems: количество задач, которые можно держать одновременно
            - started_at, closed_at: даты начала и окончания
            - rule_type: тип правил контеста (по умолчанию ContestRuleType.DEFAULT)
            - flag_user_can_have_negative_points: разрешены ли отрицательные баллы (по умолчанию False)

    Raises:
        PermissionDenied: Если у пользователя нет прав на редактирование контеста (возвращает 403).
        EntityDoesNotExist: Если контест с указанным ID не существует (возвращает 404).
    """

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
) -> JSONResponse:
    """
    Получает базовую информацию о контесте для участника.

    Доступно только участникам контеста.
    Возвращает общедоступные данные: название, ID и временные рамки контеста.

    Args:
        contest_id (int): ID контеста, информация о котором запрашивается (передаётся в query).
        user (User): Авторизованный пользователь (определяется по JWT).
        contest_service (IContestService): Сервис для получения данных контеста.

    Returns:
        JSONResponse: Объект с информацией о контесте в поле `body`:

    Raises:
        PermissionDenied: Если пользователь не является участником контеста (возвращает 403).
        EntityDoesNotExist: Если контест с указанным ID не существует (возвращает 404).
    """

    result: ContestInfoForContestant = (
        await contest_service.contest_info_for_contestant(
            user_id=user.id,
            contest_id=contest_id,
        )
    )
    result = result.model_dump()

    return JSONResponse({'body': result})


@router.get(
    path="/standings",
    response_model=ContestStandings,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def contest_standings(
        contest_id: int = Query(...),
        user: User = Depends(get_user),
        contest_service: IContestService = Depends(get_contest_service),
) -> ContestStandings:
    """
    Возвращает таблицу результатов (турнирную таблицу) контеста.

    Доступно участникам контеста и пользователям с правами на просмотр standings.
    Содержит список участников с их баллами, именами и местами в рейтинге.

    Args:
        contest_id (int): ID контеста, таблица которого запрашивается (в query-параметре).
        user (User): Авторизованный пользователь (определяется по JWT).
        contest_service (IContestService): Сервис для получения данных таблицы.
        permission_service (IPermissionService): Сервис для проверки прав доступа.

    Returns:
        ContestStandings: Объект с информацией:
            - contest_id: ID контеста
            - name: название контеста
            - started_at, closed_at: даты начала и окончания
            - standings: список участников с баллами и местами
            - use_cache: флаг, указывающий, используются ли кэшированные данные (по умолчанию False)

        Каждый участник в `standings.body` содержит:
            - contestant_id: ID участника
            - name: имя
            - points: набранные баллы
            - rank: место в таблице

    Raises:
        PermissionDenied: Если пользователь не имеет прав на просмотр таблицы (возвращает 403).
        EntityDoesNotExist: Если контест с указанным ID не существует (возвращает 404).
    """

    result: ContestStandings = (
        await contest_service.contest_standings(
            user_id=user.id,
            contest_id=contest_id,
        )
    )
    result = result.model_dump()

    return result


@router.get(
    path="/submissions",
    response_model=ContestSubmissions,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def contest_submissions(
        contest_id: int = Query(...),
        user: User = Depends(get_user),
        contest_service: IContestService = Depends(get_contest_service),
) -> ContestSubmissions:
    """
    Возвращает список посылок участников указанного контеста.

    Доступно участникам контеста и пользователям с правами на просмотр таблицы результатов

    Args:
        contest_id (int): ID контеста, посылки которого запрашиваются (передаётся в query).
        user (User): Авторизованный пользователь (определяется по JWT).
        contest_service (IContestService): Сервис для получения данных о посылках.
        permission_service (IPermissionService): Сервис для проверки прав доступа.

    Returns:
        ContestSubmissions: Объект с информацией:
            - contest_id: ID контеста
            - name: название
            - started_at, closed_at: даты начала и окончания
            - submissions: список посылок участников
            - use_cache: флаг, используется ли кэширование (по умолчанию False)
            - show_last_n_submissions: количество последних посылок, отображаемых в выдаче

        Каждая посылка в `submissions.body` содержит:
            - contestant_id: ID участника
            - contestant_name: имя участника
            - problem_card: информация о карточке с задачей (название, цена)
            - verdict: вердикт посылки

    Raises:
        PermissionDenied: Если у пользователя нет прав на просмотр (возвращает 403).
        EntityDoesNotExist: Если контест с указанным ID не существует (возвращает 404).
    """

    result: ContestSubmissions = (
        await contest_service.contest_submissions(
            user_id=user.id,
            contest_id=contest_id,
        )
    )
    result = result.model_dump()

    return result
