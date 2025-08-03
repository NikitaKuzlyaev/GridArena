from fastapi import Form


class CustomLoginForm:
    """
    Кастомная форма авторизации для платформы.

    Помимо стандартных полей — имени пользователя и пароля — включает дополнительное поле `domain_number`.
    Это поле определяет контекст входа:
      - Если `domain_number` равен 0 — пользователь авторизуется как обычный пользователь сайта.
      - Если `domain_number` больше 0 — пользователь авторизуется как участник соревнования с ID, равным `domain_number`.

    Поля:
        domain_number (int): Номер домена (0 — пользователь сайта, >0 — участник соревнования).
        username (str): Имя пользователя.
        password (str): Пароль.
    """

    def __init__(
            self,
            domain_number: int = Form(...),
            username: str = Form(...),
            password: str = Form(...),
    ):
        self.domain_number = domain_number
        self.username = username
        self.password = password
