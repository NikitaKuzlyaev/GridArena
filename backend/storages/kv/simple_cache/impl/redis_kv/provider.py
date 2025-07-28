from typing import Dict, Tuple

import redis.asyncio as redis

from backend.configuration.settings import settings
from backend.storages.kv.simple_cache.impl.redis_kv.redis_kv import RedisKeyValueSimpleCache
from backend.storages.kv.simple_cache.interface import IKeyValueSimpleCache

BASE_HOST = settings.REDIS_KV_SIMPLE_CACHE_HOST
BASE_PORT = settings.REDIS_KV_SIMPLE_CACHE_PORT
BASE_DB = settings.REDIS_KV_SIMPLE_CACHE_DB

# Хранилище инстансов по (host, port, db)
_redis_kv_instances: Dict[Tuple[str, int, int], RedisKeyValueSimpleCache] = {}


def get_redis_kv_simple_cache(
        host: str = BASE_HOST,
        port: int = BASE_PORT,
        db: int = BASE_DB,
) -> IKeyValueSimpleCache:
    key = (host, port, db)

    if key in _redis_kv_instances:
        return _redis_kv_instances[key]

    redis_client = redis.Redis(
        host=host,
        port=port,
        db=db,
        decode_responses=False
    )

    instance = RedisKeyValueSimpleCache(redis_client)
    _redis_kv_instances[key] = instance
    return instance
