from backend.core.utilities.methods.registry import function_registry
from backend.storages.kv.simple_cache.impl.redis_kv.provider import get_redis_kv_simple_cache


@function_registry.register_function(
    alias="backend.core.services.proxies.cache.cache_method_result_proxy"
)
async def cache_method_result_proxy(
        void_name: str,
        void_result: str,
        ttl_s: int = 1000,
):
    cache_instance = get_redis_kv_simple_cache(db=1)
    await cache_instance.set_str_value_by_str_key(void_name, void_result, expires_in_seconds=ttl_s)
