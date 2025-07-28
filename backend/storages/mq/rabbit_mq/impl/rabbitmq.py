import inspect
import json
from typing import Optional, Callable

import aio_pika

from backend.core.utilities.loggers.log_decorator import log_calls
from backend.core.utilities.methods.registry import function_registry
from backend.storages.mq.rabbit_mq.interface import IVoidMessageQueue


class RabbitMQVoidHandler(IVoidMessageQueue):
    def __init__(
            self,
            rabbitmq_url: str,
            queue_name: str,
    ):
        """
        :param rabbitmq_url: URI подключения к RabbitMQ (например, "amqp://guest:guest@localhost/")
        :param queue_name: Название очереди, в которую будут публиковаться задания
        """
        self._url = rabbitmq_url
        self._queue_name = queue_name
        self._connection: Optional[aio_pika.RobustConnection] = None
        self._channel: Optional[aio_pika.abc.AbstractChannel] = None
        self._queue: Optional[aio_pika.abc.AbstractQueue] = None

    @log_calls
    async def connect(self):
        """
        Устанавливает соединение с RabbitMQ и создает очередь.
        """
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(self._queue_name, durable=True)

    @log_calls
    async def add_void(
            self,
            void: Callable,
            callback: Callable,
            callback_params: dict = None,
            use_void_result_in_callback_params: bool = True,
            **kwargs,
    ) -> None:
        """
        Публикует функцию с параметрами в очередь для асинхронного исполнения.

        :param void: Основная функция, которую нужно выполнить (обязана быть зарегистрирована в function_registry)
        :param callback: Функция, вызываемая после завершения `void` (тоже должна быть зарегистрирована)
        :param callback_params: Аргументы, передаваемые в callback (дополнительно к результату `void`)
        :param use_void_result_in_callback_params: Передавать ли результат `void` в callback
        """
        if self._channel is None:
            await self.connect()

        void_name = f"{void.__module__}.{void.__qualname__}"
        callback_name = f"{callback.__module__}.{callback.__qualname__}" if callback else None

        # args и kwargs должны быть json-сериализуемыми
        payload = {
            "func_name": void_name,
            "kwargs": kwargs,
            "callback_name": callback_name,
            "callback_params": callback_params or {},
            "use_void_result_in_callback_params": use_void_result_in_callback_params,
        }

        body = json.dumps(payload).encode("utf-8")

        await self._channel.default_exchange.publish(
            aio_pika.Message(body=body),
            routing_key=self._queue_name,
        )

    @log_calls
    async def consume_forever(self):
        """
        Запускает бесконечную обработку сообщений из очереди.

        Каждое сообщение передается в `_handle_message`, где вызывается функция и (если указано) callback.
        """
        if self._queue is None:
            await self.connect()

        async with self._queue.iterator() as queue_iter:
            async for message in queue_iter:
                try:
                    await self._handle_message(message.body)
                except Exception as e:
                    print(f"Error processing message: {e}")
                finally:
                    await message.ack()

    @log_calls
    async def _handle_message(
            self,
            body: bytes
    ) -> None:
        """
        Внутренняя функция обработки одного сообщения.

        :param body: Сырые данные сообщения (JSON, сериализованное через `add_void`)
        """
        payload = json.loads(body.decode("utf-8"))

        func_name = payload["func_name"]
        kwargs = payload["kwargs"]
        callback_name = payload.get("callback_name")
        callback_params = payload.get("callback_params", {})
        use_result = payload.get("use_void_result_in_callback_params", True)

        func = function_registry.get_function(func_name)

        if func is None:
            raise RuntimeError(f"Function {func_name} is not registered in <function_registry>")

        if inspect.iscoroutinefunction(func):
            result = await func(**kwargs)
        else:
            result = func(**kwargs)

        if callback_name:
            callback = function_registry.get_function(callback_name)
            if callback is None:
                raise RuntimeError(f"Callback function {callback_name} is not registered")

            if inspect.iscoroutinefunction(callback):
                if use_result:
                    await callback(void_result=result.model_dump_json(), **callback_params)
                else:
                    await callback(**callback_params)
            else:
                if use_result:
                    callback(void_result=result.model_dump_json(), **callback_params)
                else:
                    callback(**callback_params)
