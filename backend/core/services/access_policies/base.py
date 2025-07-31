from typing import Protocol, Any

from backend.core.utilities.exceptions.permission import PermissionDenied


class AccessPolicy(Protocol):
    """
    Протокол для описания политики доступа.

    Классы, реализующие этот протокол, должны определять правила доступа
    к определённым ресурсам или действиям на основе предоставленных данных.

    Этот класс подразумевает наследование от него низкоуровневых классов с
    правилами проверки доступа для каждого домена.

    Например, ContestAccessPolicy(AccessPolicy) - класс, определяющий методы проверки доступа
    пользователя к ресурсам, предоставляемых реализацией IContestService (например, ContestService)
    """
    ...

    @staticmethod
    def _raise_if(condition: bool, msg: str, ex_type: type[Exception] = PermissionDenied) -> None:
        if condition:
            raise ex_type(msg)
