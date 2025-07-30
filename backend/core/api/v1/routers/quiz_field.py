import fastapi
from fastapi import (
    Body,
    Depends,
    Query,
)

from backend.core.dependencies.authorization import get_user
from backend.core.models import User
from backend.core.schemas.quiz_field import (
    QuizFieldId,
    QuizFieldUpdateRequest,
    QuizFieldInfoForEditor,
    QuizFieldInfoForContestant,
)
from backend.core.services.interfaces.permission import IPermissionService
from backend.core.services.interfaces.quiz_field import IQuizFieldService
from backend.core.services.providers.permission import get_permission_service
from backend.core.services.providers.quiz_field import get_quiz_field_service
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from backend.core.utilities.exceptions.permission import PermissionDenied

router = fastapi.APIRouter(prefix="/quiz-field", tags=["quiz-field"])


@router.patch(
    path="/",
    response_model=QuizFieldId,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        EntityDoesNotExist: (404, None),
    }
)
async def update_quiz_field(
        params: QuizFieldUpdateRequest = Body(...),
        user: User = Depends(get_user),
        quiz_service: IQuizFieldService = Depends(get_quiz_field_service),
) -> QuizFieldId:
    """
    Обновляет параметры поля (сетку карточек задач).

    Позволяет изменить количество строк и столбцов в сетке задач.
    При уменьшении размера лишние карточки недоступны, но не удаляются.

    Args:
        params (QuizFieldUpdateRequest): Новые параметры поля:
            - quiz_field_id: ID поля, которое необходимо обновить
            - number_of_rows: новое количество строк (от 1 до 8)
            - number_of_columns: новое количество столбцов (от 1 до 8)
        user (User): Авторизованный пользователь (определяется по JWT).
        quiz_service (IQuizFieldService): Сервис для обновления поля.

    Returns:
        QuizFieldId: Объект с подтверждением обновления:
            - quiz_field_id: ID обновлённого поля

    Raises:
        EntityDoesNotExist: Если поле с указанным ID не существует (возвращает 404).

    Примечание:
        Изменение размера сетки может повлиять на существующие карточки:
        - При уменьшении — карточки за пределами новой сетки будут недоступны.
        - При увеличении — новые ячейки остаются пустыми.
        Изменения на идущем контесте могут быть непредсказуемыми! (логика может меняться со временем)
    """

    # todo: добавить проверку прав

    result: QuizFieldId = (
        await quiz_service.update_quiz_field(
            **params.model_dump(),
        )
    )
    result = result.model_dump()

    return result


@router.get(
    path="/info-editor",
    response_model=QuizFieldInfoForEditor,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def quiz_field_info_for_editor(
        contest_id: int = Query(...),
        user: User = Depends(get_user),
        quiz_field_service: IQuizFieldService = Depends(get_quiz_field_service),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> QuizFieldInfoForEditor:
    """
    Получает полную информацию о поле для редактора контеста.

    Возвращает структуру сетки (количество строк и столбцов) и список всех карточек задач с их данными.
    Доступно только пользователям с правами на редактирование контеста.

    Args:
        contest_id (int): ID контеста, поле которого запрашивается (в query).
        user (User): Авторизованный пользователь (определяется по JWT).
        quiz_field_service (IQuizFieldService): Сервис для получения данных поля.
        permission_service (IPermissionService): Сервис для проверки прав на редактирование контеста.

    Returns:
        QuizFieldInfoForEditor: Объект с информацией:
            - quiz_field_id: ID поля
            - number_of_rows: количество строк в сетке
            - number_of_columns: количество столбцов
            - problem_cards: список карточек, каждая содержит:
                - problem_card_id: ID карточки
                - problem: ID связанной задачи
                - row, column: позиция в сетке
                - category_price: стоимость задачи
                - category_name: название категории

    Raises:
        PermissionDenied: Если у пользователя нет прав на редактирование контеста (возвращает 403).
        EntityDoesNotExist: Если контест или поле не существуют (возвращает 404).

    Примечание:
        Этот эндпоинт используется в интерфейсе редактирования контеста для отображения
        и настройки сетки задач. Включает только публичные метаданные карточек — ответы задач не возвращаются.
    """
    await permission_service.raise_if_not_all([
        lambda: permission_service.check_permission_for_edit_contest(user_id=user.id, contest_id=contest_id),
    ])

    result: QuizFieldInfoForEditor = (
        await quiz_field_service.quiz_field_info_for_editor(
            user_id=user.id,
            contest_id=contest_id,
        )
    )
    result = result.model_dump()

    return result


@router.get(
    path="/info-contestant",
    response_model=QuizFieldInfoForContestant,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        PermissionDenied: (403, None),
        EntityDoesNotExist: (404, None),
    }
)
async def quiz_field_info_for_contestant(
        user: User = Depends(get_user),
        quiz_field_service: IQuizFieldService = Depends(get_quiz_field_service),
) -> QuizFieldInfoForContestant:
    """
    Получает информацию о поле для участника контеста.

    Возвращает структуру сетки (размеры) и состояние каждой карточки задачи:
    открыта ли она, доступна ли для выбора, решена ли и т.д. Используется в интерфейсе участника для отображения игрового поля .

    Args:
        user (User): Авторизованный участник (определяется по JWT).
        quiz_field_service (IQuizFieldService): Сервис для получения данных поля.

    Returns:
        QuizFieldInfoForContestant: Объект с информацией:
            - quiz_field_id: ID поля
            - number_of_rows: количество строк в сетке
            - number_of_columns: количество столбцов
            - problem_cards: список карточек с информацией:
                - problem_card_id: ID карточки
                - problem: ID задачи
                - status: текущий статус карточки (OPEN, SOLVING, SOLVED и др.)
                - is_open_for_buy: доступна ли карточка для выбора (с учётом правил контеста)
                - row, column: позиция в сетке
                - category_price: стоимость задачи
                - category_name: название категории

    Raises:
        PermissionDenied: Если пользователь не является участником контеста (возвращает 403).
        EntityDoesNotExist: Если у пользователя нет активного участия в контесте или поле не существует (возвращает 404).

    Примечание:
        Ответ содержит только ту информацию, которая разрешена к показу участнику.
    """
    result: QuizFieldInfoForContestant = (
        await quiz_field_service.quiz_field_info_for_contestant(
            user_id=user.id,
        )
    )
    result = result.model_dump()

    return result
