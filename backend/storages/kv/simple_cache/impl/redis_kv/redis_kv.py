from redis import Redis

from backend.storages.kv.simple_cache.interface import IKeyValueSimpleCache


class RedisKeyValueSimpleCache(IKeyValueSimpleCache):
    def __init__(
            self,
            redis_client: Redis,
    ) -> None:
        self._redis = redis_client

    async def get_str_value_by_str_key(
            self,
            key: str,
    ) -> str | None:
        value = await self._redis.get(key)
        if value is None:
            return None
        return value.decode('utf-8')

    async def set_str_value_by_str_key(
            self,
            key: str,
            value: str,
            expires_in_seconds: int,
    ) -> None:
        await self._redis.set(key, value, ex=expires_in_seconds)
