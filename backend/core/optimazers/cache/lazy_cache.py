import functools
import hashlib
import json
from datetime import datetime

from backend.core.schemas.contest import ContestStandings
from backend.core.utilities.methods.registry import function_registry
from backend.storages.kv.simple_cache.impl.redis_kv.provider import get_redis_kv_simple_cache
from backend.storages.kv.simple_cache.interface import IKeyValueSimpleCache
from backend.storages.mq.rabbit_mq.impl.provider import get_rabbit_mq
from backend.storages.mq.rabbit_mq.interface import IVoidMessageQueue


def _make_key(class_name, func_name, kwargs) -> str:
    raw = f"{class_name}.{func_name}:{kwargs}"
    return hashlib.sha256(raw.encode()).hexdigest()


class LazyCache:

    def __init__(
            self,
            cache_instance: IKeyValueSimpleCache,
            message_queue_instance: IVoidMessageQueue | None = None,
    ):
        self._cache_instance = cache_instance
        self._message_queue_instance = message_queue_instance

    def decorator_fabric(
            self,
            get_from_cache_not_later_than_s: int = 1,
            result_cached_time_s: int = 2,
            refresh_cache_if_ttl_less_than_s: int = -1,
    ):
        """

        """
        # Если возможна делегация на обновление кеша, то должна быть объявлена очередь сообщений
        if refresh_cache_if_ttl_less_than_s > 0 and self._message_queue_instance is None:
            raise ValueError("<message_queue_instance> cannot be None when <void_method_at_the_end> is True")

        def decorator(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):

                # Регистрация функции в регистре, чтобы потом найти ее при выполнении и в callback
                function_registry.register_function(func)

                class_name = args[0].__class__.__name__ if args else None
                func_name = func.__name__
                void_name = _make_key(class_name, func_name, kwargs)

                cached_result_with_time_when_set = (
                    await self._cache_instance.get_str_value_by_str_key_with_time_when_set(
                        key=void_name,
                    )
                )
                # Кешированный результат вызова и время когда он был произведен
                cached_result, time_when_set = cached_result_with_time_when_set
                flag_used_cache = True  # Флаг: было ли значение получено из кеша

                if cached_result is None:
                    # Если результата нет в кеше, то получаем его напрямую
                    res: ContestStandings = await func(*args, **kwargs)
                    flag_used_cache = False

                    # Обновление кеша
                    await self._cache_instance.set_str_value_by_str_key(
                        key=void_name,
                        value=res.model_dump_json(),
                        expires_in_seconds=result_cached_time_s,
                    )
                    cached_result = res.model_dump_json()

                dt_s = None
                if time_when_set:
                    dt = datetime.now() - time_when_set
                    dt_s = dt.total_seconds()

                # Нужно отправить задачу на обновление кеша тогда, когда одновременно:
                #   * Есть указание сделать это (refresh_cache_if_ttl_less_than_ms > 0)
                #   * Нет временной метку установки кеша (истекла или ее не было)
                # или значение было установленно достаточно давно (dt_ms >= get_from_cache_not_later_than_ms)
                if (refresh_cache_if_ttl_less_than_s > 0 and
                        (not dt_s or dt_s >= get_from_cache_not_later_than_s)
                ):
                    await self._message_queue_instance.add_void(
                        void=func,
                        callback=function_registry.get_function(
                            "backend.core.services.proxies.cache.cache_method_result_proxy"
                        ),
                        callback_params={'void_name': void_name, 'ttl_s': result_cached_time_s},
                        use_void_result_in_callback_params=True,
                        **kwargs,
                    )

                parsed = json.loads(cached_result)
                result = ContestStandings.model_validate(parsed)
                result.use_cache = flag_used_cache

                return result

            return async_wrapper

        return decorator


def get_lazy_cache(
        cache_instance: IKeyValueSimpleCache = get_redis_kv_simple_cache(db=1),
        message_queue_instance: IVoidMessageQueue = get_rabbit_mq(queue_name="lazy_cache"),
) -> LazyCache:
    return LazyCache(
        cache_instance=cache_instance,
        message_queue_instance=message_queue_instance,
    )


lazy_cache_optimizer = get_lazy_cache()
