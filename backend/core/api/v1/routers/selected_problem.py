import fastapi
from fastapi import (
    Body,
    Depends,
)

from backend.core.dependencies.authorization import get_user
from backend.core.models import User
from backend.core.schemas.selected_problem import (
    SelectedProblemId,
    SelectedProblemBuyRequest,
    ArraySelectedProblemInfoForContestant,
)
from backend.core.services.interfaces.selected_problem import ISelectedProblemService
from backend.core.services.providers.selected_problem import get_selected_problem_service
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from backend.core.utilities.exceptions.logic import PossibleLimitOverflow
from backend.core.utilities.exceptions.permission import PermissionDenied

router = fastapi.APIRouter(prefix="/selected-problem", tags=["selected-problem"])


@router.post(
    path="/buy",
    response_model=SelectedProblemId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
        PossibleLimitOverflow: (403, None),
    }
)
async def buy_problem(
        params: SelectedProblemBuyRequest = Body(...),
        user: User = Depends(get_user),
        selected_problem_service: ISelectedProblemService = Depends(get_selected_problem_service)
) -> SelectedProblemId:
    """
    Выбирает («покупает») задачу для решения участником.

    Инициирует процесс решения задачи: участник тратит баллы (в зависимости от стоимости карточки).
    Доступно только участникам активного контеста.

    Args:
        params (SelectedProblemBuyRequest): Параметры запроса:
            - problem_card_id: ID карточки задачи, которую участник хочет выбрать
        user (User): Авторизованный участник (определяется по JWT).
        selected_problem_service (ISelectedProblemService): Сервис для управления выбранными задачами.

    Returns:
        SelectedProblemId: Объект с подтверждением:
            - selected_problem_id: уникальный ID записи о выбранной задаче

    Raises:
        PermissionDenied:
            - Если у пользователя нет прав на участие в контесте
            - Или если задача уже выбрана/решается
        EntityDoesNotExist:
            - Если карточка с указанным problem_card_id не существует
            - Или если участник не привязан к контеcту
        PossibleLimitOverflow:
            - Если превышено максимальное количество одновременно решаемых задач
            - Или если у участника недостаточно баллов для "покупки"

    Примечание:
        Операция может быть ограничена правилами контеста:
        - Максимальное число активных задач
        - Доступность карточки
        - Баланс участника должен покрывать стоимость задачи
    """
    # todo: проверка прав
    result: SelectedProblemId = (
        await selected_problem_service.buy_selected_problem(
            user_id=user.id,
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return result


@router.get(
    path="/my",
    response_model=ArraySelectedProblemInfoForContestant,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def get_contestant_selected_problems(
        user: User = Depends(get_user),
        selected_problem_service: ISelectedProblemService = Depends(get_selected_problem_service)
) -> ArraySelectedProblemInfoForContestant:
    """
    Получает список всех выбранных («купленных») задач текущего участника.

    Возвращает информацию о каждой активной или решаемой задаче, включая условие, стоимость,
    количество оставшихся попыток и другую контекстную информацию. Используется в интерфейсе участника
    для отображения текущих задач.

    Args:
        user (User): Авторизованный участник (определяется по JWT).
        selected_problem_service (ISelectedProblemService): Сервис для получения данных о выбранных задачах.

    Returns:
        ArraySelectedProblemInfoForContestant: Объект, содержащий:
            - body: список активных задач, которые участник выбрал для решения
            - rule_type: тип правил контеста (влияет на логику попыток, начисления баллов)
            - max_attempts_for_problem: максимальное количество попыток на задачу (опционально)

        Каждая задача в `body` содержит:
            - selected_problem_id: ID записи о выборе задачи
            - problem_card_id: ID карточки задачи
            - problem: вложенный объект с:
                - problem_id: ID задачи
                - statement: условие задачи
            - category_name, category_price: категория и стоимость задачи
            - created_at: время выбора задачи
            - attempts_remaining: сколько попыток осталось (если применимо)

    Raises:
        PermissionDenied: Если пользователь не является участником активного контеста (возвращает 403).
        EntityDoesNotExist: Если участник не найден или не участвует в контесте (возвращает 404).

    Примечание:
        Ответ включает только задачи, находящиеся в статусе "в работе" (SOLVING).
        Условие задачи возвращается, так как участник имеет право на его просмотр.
    """
    result: ArraySelectedProblemInfoForContestant = (
        await selected_problem_service.get_contestant_selected_problems(
            user_id=user.id,
        )
    )
    result = result.model_dump()

    return result
