from typing import Protocol


class ITokenBlacklistHandler(Protocol):

    async def move_token_to_blacklist(
            self,
            token: str,
            expires_in_seconds: int,
    ) -> None:
        ...

    async def check_token_in_blacklist(
            self,
            token: str,
    ) -> bool:
        ...
