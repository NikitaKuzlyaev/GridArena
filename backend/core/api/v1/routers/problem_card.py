import fastapi
from fastapi import (
    Body,
    Depends,
    Query,
)
from starlette.responses import JSONResponse

from backend.core.dependencies.authorization import get_user
from backend.core.models import User
from backend.core.schemas.problem_card import (
    ProblemCardId,
    ProblemCardUpdateRequest,
    ProblemCardInfoForEditor,
    ProblemCardWithProblemUpdateRequest,
    ProblemCardWithProblemCreateRequest,
)
from backend.core.services.interfaces.problem_card import IProblemCardService
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
) -> JSONResponse:
    """
    Обновляет категорию и стоимость карточки задачи (problem card).

    Доступно только пользователям с правами на редактирование данной карточки.

    Args:
        params (ProblemCardUpdateRequest): Новые данные для карточки:
            - problem_card_id: ID карточки, которую необходимо обновить
            - category_name: новое название категории (до 32 символов)
            - category_price: новая стоимость задачи (от 0 до 10000 баллов)
        user (User): Авторизованный пользователь (определяется по JWT).
        problem_card_service (IProblemCardService): Сервис для обновления карточки.

    Returns:
        JSONResponse: Объект с обновлённым ID карточки в поле `body`

    Raises:
        PermissionDenied: Если у пользователя нет прав на редактирование этой карточки (возвращает 403).
        EntityDoesNotExist: Если карточка с указанным problem_card_id не существует (возвращает 404).

    Примечание:
        Изменение стоимости может повлиять на начисление баллов при решении.
        Логика применения изменений на идущем контесте может быть непредсказуемой. (может меняться)
    """

    result: ProblemCardId = (
        await problem_card_service.update_problem_card(
            user_id=user.id,
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
) -> ProblemCardInfoForEditor:
    """
    Получает полную информацию о карточке задачи для редактора (администратора/организатора).

    Включает как данные самой карточки (позиция, категория, цена), так и связанные данные задачи —
    условие и ответ. Доступно только пользователям с правами на редактирование этой карточки.

    Args:
        problem_card_id (int): ID карточки задачи, информация о которой запрашивается (в query).
        user (User): Авторизованный пользователь (определяется по JWT).
        problem_card_service (IProblemCardService): Сервис для получения данных карточки.

    Returns:
        ProblemCardInfoForEditor: Объект с полной информацией:
            - problem_card_id: ID карточки
            - row, column: позиция в сетке задач
            - category_name: название категории
            - category_price: стоимость задачи в баллах
            - problem: вложенный объект с информацией о задаче:
                - problem_id: ID задачи
                - statement: условие задачи
                - answer: правильный ответ

    Raises:
        PermissionDenied: Если у пользователя нет прав на редактирование этой карточки (возвращает 403).
        EntityDoesNotExist: Если карточка с указанным ID не существует (возвращает 404).

    Примечание:
        Этот эндпоинт предназначен для интерфейса редактирования — например, при настройке контеста.
        Ответ содержит чувствительные данные (ответ на задачу), поэтому доступ строго ограничен.
        Изменения на идущем контесте могут быть непредсказуемыми! (логика может меняться со временем)
    """

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
async def problem_card_update_with_problem(
        params: ProblemCardWithProblemUpdateRequest = Body(...),
        user: User = Depends(get_user),
        problem_card_service: IProblemCardService = Depends(get_problem_card_service),
) -> ProblemCardId:
    """
    Обновляет карточку задачи и связанные с ней данные задачи (условие и ответ) в одном запросе.

    Позволяет синхронно изменить:
    - метаданные карточки (категория, цена)
    - содержание самой задачи (условие и ответ)

    Доступно только пользователям с правами на редактирование **и карточки, и задачи**.

    Args:
        params (ProblemCardWithProblemUpdateRequest): Данные для обновления:
            - problem_card_id: ID карточки
            - problem_id: ID связанной задачи
            - category_name: новое название категории (до 32 символов)
            - category_price: новая стоимость (0–10000)
            - statement: новое условие задачи (до 2048 символов)
            - answer: новый правильный ответ (до 32 символов)
        user (User): Авторизованный пользователь (определяется по JWT).
        problem_card_service (IProblemCardService): Сервис для обновления карточки и задачи.

    Returns:
        ProblemCardId: Объект с подтверждением обновления:
            - problem_card_id: ID обновлённой карточки

    Raises:
        PermissionDenied:
            - Если у пользователя нет прав на редактирование карточки или задачи (возвращает 403).
        EntityDoesNotExist:
            - Если карточка или задача с указанным ID не существуют (возвращает 404).
    """

    result: ProblemCardId = (
        await problem_card_service.update_problem_card_with_problem(
            user_id=user.id,
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
async def problem_card_create_with_problem(
        params: ProblemCardWithProblemCreateRequest = Body(...),
        user: User = Depends(get_user),
        problem_card_service: IProblemCardService = Depends(get_problem_card_service),
) -> ProblemCardId:
    """
    Создаёт новую карточку задачи и связанную с ней задачу в одном запросе.

    Требует прав на редактирование поля (quiz field), к которому относится карточка.

    Args:
        params (ProblemCardWithProblemCreateRequest): Данные для создания:
            - quiz_field_id: ID поля, куда добавляется карточка
            - row, column: позиция карточки в сетке
            - category_name: название категории (до 32 символов)
            - category_price: стоимость задачи в баллах (0–10000)
            - statement: условие задачи (до 2048 символов)
            - answer: правильный ответ (до 32 символов)
        user (User): Авторизованный пользователь (определяется по JWT).
        problem_card_service (IProblemCardService): Сервис для создания карточки и задачи.

    Returns:
        ProblemCardId: Объект с ID созданной карточки:
            - problem_card_id: уникальный идентификатор новой карточки

    Raises:
        PermissionDenied:
            - Если у пользователя нет прав на редактирование указанного поля викторины (возвращает 403).
        EntityDoesNotExist:
            - Если поле викторины (quiz_field_id) не существует (возвращает 404).
    """

    result: ProblemCardId = (
        await problem_card_service.create_problem_card_with_problem(
            user_id=user.id,
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return result
