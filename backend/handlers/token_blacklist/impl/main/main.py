from backend.core.utilities.loggers.log_decorator import log_calls
from backend.handlers.token_blacklist.interface import ITokenBlacklistHandler
from backend.storages.kv.simple_cache.interface import IKeyValueSimpleCache


class TokenBlacklistHandler(ITokenBlacklistHandler):
    def __init__(
            self,
            kv_storage: IKeyValueSimpleCache,
    ):
        self._kv_storage = kv_storage

    @log_calls
    async def move_token_to_blacklist(
            self,
            token: str,
            expires_in_seconds: int,
    ) -> None:
        await self._kv_storage.set_str_value_by_str_key(
            key=token,
            value=token,
            expires_in_seconds=expires_in_seconds,
        )

    @log_calls
    async def check_token_in_blacklist(
            self,
            token: str,
    ) -> bool:
        res: str | None = (
            await self._kv_storage.get_str_value_by_str_key(
                key=token,
            )
        )
        if res:
            return True
        return False
