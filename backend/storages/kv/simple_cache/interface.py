from typing import Protocol, runtime_checkable


@runtime_checkable
class IKeyValueSimpleCache(Protocol):

    async def get_str_value_by_str_key(
            self,
            key: str,
    ) -> str | None:
        ...

    async def set_str_value_by_str_key(
            self,
            key: str,
            value: str,
            expires_in_seconds: int,
    ) -> None:
        ...
