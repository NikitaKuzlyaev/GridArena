from typing import Callable

from backend.core.utilities.loggers.log_decorator import log_calls


class FunctionRegistry:

    def __init__(self):
        self._function_registry: dict[str, Callable] = {}

    @log_calls
    def register_function(
            self,
            alias: str | None = None,
    ) -> Callable:

        def decorator(func: Callable) -> Callable:
            if alias is None:
                name = f"{func.__module__}.{func.__qualname__}"
            else:
                name = alias
            self._function_registry[name] = func
            return func

        return decorator

    @log_calls
    def get_function(self, func_name: str) -> Callable:
        return self._function_registry.get(func_name)


function_registry = FunctionRegistry()
