import datetime
from typing import Protocol, runtime_checkable, Tuple, Optional


@runtime_checkable
class IKeyValueSimpleCache(Protocol):

    async def get_str_value_by_str_key(
            self,
            key: str,
    ) -> str | None:
        ...

    async def get_str_value_by_str_key_with_time_when_set(
            self,
            key: str,
    ) -> Tuple[Optional[str], Optional[datetime.datetime]]:
        ...

    async def get_time_when_set_str_key(
            self,
            key: str,
    ) -> datetime.datetime | None:
        ...

    async def set_str_value_by_str_key(
            self,
            key: str,
            value: str,
            expires_in_seconds: int,
    ) -> None:
        ...
