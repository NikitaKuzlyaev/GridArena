from backend.configuration.settings import settings
from backend.storages.mq.rabbit_mq.impl.rabbitmq import RabbitMQVoidHandler
from backend.storages.mq.rabbit_mq.interface import IVoidMessageQueue

BASE_URL = settings.RMQ_AMQP_URL
BASE_QUEUE = "base_queue"


def get_rabbit_mq(
        rabbitmq_url: str = BASE_URL,
        queue_name: str = BASE_QUEUE,
) -> IVoidMessageQueue:
    return RabbitMQVoidHandler(
        rabbitmq_url=rabbitmq_url,
        queue_name=queue_name,
    )
