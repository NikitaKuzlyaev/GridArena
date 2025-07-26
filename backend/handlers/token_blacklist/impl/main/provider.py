from fastapi import Depends

from backend.handlers.token_blacklist.impl.main.main import TokenBlacklistHandler
from backend.handlers.token_blacklist.interface import ITokenBlacklistHandler
from backend.storages.kv.simple_cache.impl.redis_kv.provider import get_redis_kv_simple_cache
from backend.storages.kv.simple_cache.impl.redis_kv.redis_kv import RedisKeyValueSimpleCache


async def get_token_blacklist_handler(
        kv_storage: RedisKeyValueSimpleCache = Depends(get_redis_kv_simple_cache),
) -> ITokenBlacklistHandler:
    return TokenBlacklistHandler(
        kv_storage=kv_storage,
    )
