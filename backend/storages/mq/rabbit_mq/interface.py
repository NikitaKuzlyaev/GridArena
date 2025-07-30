from typing import (
    Protocol,
    Callable,
)


class IVoidMessageQueue(Protocol):

    async def add_void(
            self,
            void: Callable,
            callback: Callable,
            callback_params: dict = None,
            use_void_result_in_callback_params: bool = True,
            **kwargs,
    ) -> None:
        ...

    async def connect(self):
        ...

    async def consume_forever(self):
        ...
