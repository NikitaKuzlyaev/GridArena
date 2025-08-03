import functools
import hashlib
import json
from datetime import datetime
from typing import Type, Callable, Awaitable, Any

from pydantic import BaseModel

from backend.core.utilities.methods.registry import function_registry
from backend.storages.kv.simple_cache.interface import IKeyValueSimpleCache
from backend.storages.mq.rabbit_mq.interface import IVoidMessageQueue


def _make_key(class_name: str | None, func_name: str, kwargs: dict) -> str:
    raw = f"{class_name}.{func_name}:{json.dumps(kwargs, sort_keys=True)}"
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
            model_class: Type[BaseModel],  # Тип модели результата
            get_from_cache_not_later_than_s: int = 1,
            result_cached_time_s: int = 2,
            refresh_cache_if_ttl_less_than_s: int = -1,
    ) -> Callable[
        [Callable[..., Awaitable[Any]]],
        Callable[..., Awaitable[BaseModel]]
    ]:
        """
        Создаёт декоратор, оборачивающий асинхронные функции с кешированием результата и возможностью
        ленивого обновления кеша через очередь сообщений.

        Args:
            model_class (Type[BaseModel]): Класс модели, для валидации и десериализации результата.
            get_from_cache_not_later_than_s (int): Максимальный "возраст" значения в кеше, допустимый для использования.
            result_cached_time_s (int): Время жизни закешированного значения.
            refresh_cache_if_ttl_less_than_s (int): Если кеш устарел дольше указанного порога — инициировать обновление через MQ.
                Если ≤ 0 — ленивое обновление отключено.

        Raises:
            ValueError: Если включено ленивое обновление (refresh_cache_if_ttl_less_than_s > 0),
                        но не передана очередь сообщений.
        """

        if refresh_cache_if_ttl_less_than_s > 0 and self._message_queue_instance is None:
            raise ValueError(
                "<message_queue_instance> cannot be None when refresh_cache_if_ttl_less_than_s is set"
            )

        def decorator(
                func: Callable[..., Awaitable[Any]]
        ) -> Callable[..., Awaitable[BaseModel]]:

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs) -> BaseModel:

                function_registry.register_function(func)

                class_name = args[0].__class__.__name__ if args else None
                func_name = func.__name__
                cache_key = _make_key(class_name, func_name, kwargs)

                cached_result_with_time_when_set = await self._cache_instance.get_str_value_by_str_key_with_time_when_set(
                    key=cache_key,
                )
                cached_result, time_when_set = cached_result_with_time_when_set
                used_cache = True

                if cached_result is None:
                    # Если нет в кеше — вызываем функцию и кешируем результат
                    res = await func(*args, **kwargs)
                    used_cache = False

                    await self._cache_instance.set_str_value_by_str_key(
                        key=cache_key,
                        value=res.model_dump_json(),
                        expires_in_seconds=result_cached_time_s,
                    )
                    cached_result = res.model_dump_json()

                dt_s = None
                if time_when_set:
                    dt = datetime.now() - time_when_set
                    dt_s = dt.total_seconds()

                should_refresh = (
                        refresh_cache_if_ttl_less_than_s > 0 and
                        (dt_s is None or dt_s >= get_from_cache_not_later_than_s)
                )
                if should_refresh:
                    await self._message_queue_instance.add_void(
                        void=func,
                        callback=function_registry.get_function(
                            "backend.core.services.proxies.cache.cache_method_result_proxy"
                        ),
                        callback_params={'void_name': cache_key, 'ttl_s': result_cached_time_s},
                        use_void_result_in_callback_params=True,
                        **kwargs,
                    )

                parsed = json.loads(cached_result)
                result = model_class.model_validate(parsed)
                # Добавляем атрибут, чтобы сообщить, откуда взялось значение
                setattr(result, "use_cache", used_cache)

                return result

            return async_wrapper

        return decorator


# Пример создания экземпляра для общего кеша
def get_lazy_cache(
        cache_instance: IKeyValueSimpleCache,
        message_queue_instance: IVoidMessageQueue,
) -> LazyCache:
    return LazyCache(
        cache_instance=cache_instance,
        message_queue_instance=message_queue_instance,
    )

# Использование:
# lazy_cache = get_lazy_cache(...)
# @lazy_cache.decorator_fabric(model_class=ContestStandings)
# async def some_func(...): ...
