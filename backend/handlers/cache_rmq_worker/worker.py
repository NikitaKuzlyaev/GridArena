import asyncio

from backend.core.services.proxies.cache import cache_method_result_proxy
from backend.core.services.proxies.contest import contest_standings_proxy
from backend.storages.mq.rabbit_mq.impl.provider import get_rabbit_mq

cs = contest_standings_proxy
ch = cache_method_result_proxy

mq = get_rabbit_mq(queue_name="lazy_cache")


async def main():
    await mq.connect()
    await mq.consume_forever()


if __name__ == "__main__":
    asyncio.run(main())
