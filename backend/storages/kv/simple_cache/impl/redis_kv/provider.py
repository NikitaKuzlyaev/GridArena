import redis.asyncio as redis

from backend.configuration.settings import settings
from backend.storages.kv.simple_cache.impl.redis_kv.redis_kv import RedisKeyValueSimpleCache
from backend.storages.kv.simple_cache.interface import IKeyValueSimpleCache

host = settings.REDIS_KV_SIMPLE_CACHE_HOST
port = settings.REDIS_KV_SIMPLE_CACHE_PORT
db = settings.REDIS_KV_SIMPLE_CACHE_DB

_redis_kv_instance: RedisKeyValueSimpleCache | None = None


async def get_redis_kv_simple_cache() -> IKeyValueSimpleCache:
    global _redis_kv_instance

    if _redis_kv_instance:
        return _redis_kv_instance

    redis_client = redis.Redis(
        host=host,
        port=6379,
        db=0,
        decode_responses=False
    )

    _redis_kv_instance = RedisKeyValueSimpleCache(redis_client)

    return _redis_kv_instance
