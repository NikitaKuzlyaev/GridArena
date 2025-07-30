import asyncio
from typing import Annotated

import fastapi
from fastapi import (
    Depends,
    Request,
    Response,
    HTTPException,
)
from starlette.responses import JSONResponse

from backend.core.dependencies.authorization import get_user_with_access_token
from backend.core.dependencies.repository import get_repository
from backend.core.forms.authorization import CustomLoginForm
from backend.core.models.user import User
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.schemas.user import (
    SiteUserCreate,
    UserOut,
    Token,
    UserType,
)
from backend.core.services.domain import auth as auth_service
from backend.core.services.domain.auth import verify_refresh_token
from backend.core.services.security import (
    REFRESH_TOKEN_EXPIRE_MINUTES,
    create_refresh_token,
    create_access_token
)
from backend.core.utilities.exceptions.auth import TokenException
from backend.core.utilities.exceptions.database import EntityAlreadyExists
from backend.core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from backend.handlers.token_blacklist.impl.main.provider import get_token_blacklist_handler
from backend.handlers.token_blacklist.interface import ITokenBlacklistHandler

router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    path="/register",
    response_model=UserOut,
)
@async_http_exception_mapper(
    mapping={
        EntityAlreadyExists: (409, None),
    }
)
async def register(
        data: SiteUserCreate,
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> UserOut:
    """
    Регистрирует нового пользователя на сайте.

    Принимает имя пользователя и пароль, создаёт учётную запись.
    Если пользователь с таким именем уже существует, возвращается ошибка 409.

    Args:
        data (SiteUserCreate): Данные для регистрации:
            - username: Имя пользователя (должно быть уникальным в домене 0 - домен системы)
            - password: Пароль
        user_repo (UserCRUDRepository): Репозиторий для работы с пользователями в БД.

    Returns:
        UserOut: Объект с данными созданного пользователя:
            - id: Уникальный идентификатор пользователя
            - username: Имя пользователя

    Raises:
        EntityAlreadyExists: Если пользователь с таким username уже существует (код 409).
    """
    user: User = (
        await auth_service.register_site_user(
            data=data,
            user_repo=user_repo,
        )
    )
    res = UserOut(
        id=user.id,
        username=user.username,
    )
    return res


@router.post(
    path="/login",
    response_model=Token,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        TokenException: (401, None),
    }
)
async def login_for_access_token(
        response: Response,
        form_data: Annotated[CustomLoginForm, Depends()],
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> Token:
    """
    Аутентифицирует пользователя и выдаёт JWT-токены при успешном входе.

    Принимает домен, имя пользователя и пароль. При успешной аутентификации:
    - Возвращает access-токен в теле ответа
    - Устанавливает refresh-токен в защищённые HTTP-only куки

    Args:
        response (Response): Объект ответа FastAPI, используется для установки куки.
        form_data (CustomLoginForm): Данные формы входа:
            - domain_number: номер домена (0 — сайт, иначе — контест)
            - username: имя пользователя
            - password: пароль
        user_repo (UserCRUDRepository): Репозиторий для получения данных пользователя из БД.

    Returns:
        Token: Объект с:
            - access_token: JWT для аутентификации запросов
            - token_type: тип токена ("bearer")
            - user_type: тип пользователя (SITE или CONTEST), определяется по домену

    Raises:
        TokenException: Если аутентификация не удалась (неверные учётные данные) — возвращает 401.

    Куки (refresh_token):
        - Устанавливается в защищённый режим (httponly, secure, samesite="none")
        - Срок жизни: REFRESH_TOKEN_EXPIRE_MINUTES минут
        - Путь: / (доступен для всего API)

    Важно:
        Параметры secure=True и samesite="none" требуются для работы через HTTPS и кросс-доменных запросов.
        В режиме отладки могут быть изменены на менее строгие значения.
    """
    access_token: str = (
        await auth_service.authenticate_user(
            domain_number=form_data.domain_number,
            username=form_data.username,
            password=form_data.password,
            user_repo=user_repo,
        )
    )
    user: User = (
        await user_repo.get_user_by_username_and_domain(
            username=form_data.username,
            domain_number=form_data.domain_number,
        )
    )
    refresh_token: str = (
        create_refresh_token(
            data={"sub": user.uuid},
        )
    )
    max_age = REFRESH_TOKEN_EXPIRE_MINUTES

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # secure=True / ТОЛЬКО В ДЕБАГЕ!!!
        samesite="none",  # samesite="lax" / Только в ДЕБАГЕ!!!
        max_age=max_age * 60,
        path='/',
    )
    res = Token(
        access_token=access_token,
        token_type="bearer",
        user_type=UserType.SITE if user.domain_number == 0 else UserType.CONTEST,
    )
    return res


@router.post(
    path="/refresh",
    response_model=Token,
    status_code=200,
)
async def refresh_access_token(
        request: Request,
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> Token:
    """
    Обновляет access-токен с помощью refresh-токена, полученного из куки.

    Проверяет валидность refresh-токена. При успехе:
    - Генерирует новый access-токен
    - Возвращает его в теле ответа
    - Тип пользователя (SITE/CONTEST) определяется по домену

    Args:
        request (Request): HTTP-запрос, из которого извлекается refresh_token из куки.
        user_repo (UserCRUDRepository): Репозиторий для поиска пользователя по токену.

    Returns:
        Token: Новый объект с:
            - access_token: обновлённый JWT-токен доступа
            - token_type: тип токена ("bearer")
            - user_type: тип пользователя (SITE или CONTEST), определяется по domain_number

    Raises:
        HTTPException(401):
            - Если refresh_token отсутствует в куках
            - Если refresh_token недействителен или пользователь не найден

    Примечание:
        Сам refresh-токен не обновляется — используется существующий с тем же сроком жизни.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing.")

    user: User | None = (
        await verify_refresh_token(
            token=refresh_token,
            user_repo=user_repo,
        )
    )
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    new_access_token = create_access_token(
        data={"sub": user.uuid}
    )
    res = Token(
        access_token=new_access_token,
        token_type="bearer",
        user_type=UserType.SITE if user.domain_number == 0 else UserType.CONTEST,
    )
    return res


@router.post(
    path="/block-my-token",
)
async def move_user_tokens_to_blacklist(
        request: Request,
        user_with_access_token: User = Depends(get_user_with_access_token),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        token_blacklist_handler: ITokenBlacklistHandler = Depends(get_token_blacklist_handler),
) -> JSONResponse:
    """
    Добавляет текущие access и refresh токены пользователя в чёрный список.

    Используется при выходе из системы (logout). Оба токена блокируются на срок,
    вдвое превышающий время их жизни, чтобы гарантировать невозможность повторного использования.

    Процесс:
    - Извлекает refresh_token из куки
    - Проверяет соответствие пользователя в access и refresh токенах
    - Параллельно добавляет оба токена в чёрный список

    Args:
        request (Request): HTTP-запрос, из которого берётся refresh_token из куки.
        user_with_access_token (User): Текущий пользователь и его access-токен (из JWT).
        user_repo (UserCRUDRepository): Репозиторий для проверки refresh-токена.
        token_blacklist_handler (ITokenBlacklistHandler): Сервис для управления чёрным списком токенов.

    Returns:
        JSONResponse:
            { "success": True } при успешной блокировке.

    Raises:
        HTTPException(401):
            - Если refresh_token отсутствует в куках
            - Если refresh_token недействителен или пользователь не найден
        HTTPException(403):
            - Если пользователь из access-токена не совпадает с пользователем из refresh-токена
        HTTPException(503):
            - Если сервис чёрного списка временно недоступен

    Примечание:
        После успешного выполнения клиент должен удалить refresh_token из куки
        (рекомендуется дополнительным Set-Cookie с пустым значением и max_age=0).
    """
    user, access_token = user_with_access_token

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing.")

    user_from_refresh_token: User | None = (
        await verify_refresh_token(
            token=refresh_token,
            user_repo=user_repo,
        )
    )
    if not user_from_refresh_token:
        raise HTTPException(status_code=401, detail="User not found.")
    if user.username != user_from_refresh_token.username:
        raise HTTPException(status_code=403, detail="Permission denied.")

    try:
        await asyncio.gather(
            token_blacklist_handler.move_token_to_blacklist(
                token=refresh_token,
                expires_in_seconds=REFRESH_TOKEN_EXPIRE_MINUTES * 60 * 2,
            ),
            token_blacklist_handler.move_token_to_blacklist(
                token=access_token,
                expires_in_seconds=REFRESH_TOKEN_EXPIRE_MINUTES * 60 * 2,
            )
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service for check user token temporarily unavailable.")

    return JSONResponse({'success': True})
