import datetime
from typing import Tuple, Optional

from redis import Redis

from backend.storages.kv.simple_cache.interface import IKeyValueSimpleCache


class RedisKeyValueSimpleCache(IKeyValueSimpleCache):
    def __init__(
            self,
            redis_client: Redis,
            time_prefix: str = 'time_when_set',
    ) -> None:
        self._redis = redis_client
        self._time_prefix = time_prefix

    async def get_str_value_by_str_key(
            self,
            key: str,
    ) -> str | None:
        value = await self._redis.get(key)
        if value is None:
            return None
        return value.decode('utf-8')

    async def get_str_value_by_str_key_with_time_when_set(
            self,
            key: str,
    ) -> Tuple[Optional[str], Optional[datetime.datetime]]:
        value = await self.get_str_value_by_str_key(key=key)
        time_when_set = await self.get_time_when_set_str_key(key=key)
        return value, time_when_set

    async def get_time_when_set_str_key(
            self,
            key: str,
    ) -> datetime.datetime | None:
        value = await self._redis.get(self._time_prefix + key)
        if value is None:
            return None
        return datetime.datetime.fromisoformat(value.decode('utf-8'))

    async def set_str_value_by_str_key(
            self,
            key: str,
            value: str,
            expires_in_seconds: int,
    ) -> None:
        await self._redis.set(key, value, ex=expires_in_seconds)
        await self._redis.set(self._time_prefix + key, datetime.datetime.now().isoformat(), ex=expires_in_seconds)
