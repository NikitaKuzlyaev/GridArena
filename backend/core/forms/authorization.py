from fastapi import Form, HTTPException


class CustomLoginForm:
    """
    Кастомная форма авторизации для платформы.

    Помимо стандартных полей — имени пользователя и пароля — включает дополнительное поле `domain_number`.
    Это поле определяет контекст входа:
      - Если `domain_number` равен 0 — пользователь авторизуется как обычный пользователь сайта.
      - Если `domain_number` больше 0 — пользователь авторизуется как участник соревнования с ID, равным `domain_number`.

    Поля:
        domain_number (int): Номер домена (от -5 до 2*10^9).
        username (str): Имя пользователя (от 1 до 64 символов).
        password (str): Пароль (от 1 до 32 символов).
    """

    def __init__(
            self,
            domain_number: int = Form(...),
            username: str = Form(...),
            password: str = Form(...),
    ):
        # Валидация username
        if not username or len(username.strip()) == 0:
            raise HTTPException(status_code=400, detail="Username обязателен")
        if len(username) > 64:
            raise HTTPException(status_code=400, detail="Username не может быть длиннее 64 символов")

        # Валидация password
        if not password or len(password.strip()) == 0:
            raise HTTPException(status_code=400, detail="Password обязателен")
        if len(password) > 32:
            raise HTTPException(status_code=400, detail="Password не может быть длиннее 32 символов")

        # Валидация domain_number
        if domain_number < -5 or domain_number > 2 * 10 ** 9:
            raise HTTPException(status_code=400, detail="Domain number должен быть от -5 до 2*10^9")

        self.domain_number = domain_number
        self.username = username.strip()
        self.password = password
