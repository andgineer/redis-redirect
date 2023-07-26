"""REDIS async pubsub example."""

import asyncio
import contextlib

from redis import asyncio as aioredis

from redis_redirect.aioredis_wrapper import cache

STOPWORD = "STOP"


async def consumer(channel: aioredis.client.PubSub) -> None:
    """Listen for messages."""
    while True:
        with contextlib.suppress(asyncio.TimeoutError):
            message = await channel.get_message(ignore_subscribe_messages=True)
            if message is not None:
                print(f"(Reader) Message Received: {message}")
                if message["data"].decode() == STOPWORD:
                    print("(Reader) STOP")
                    break
            await asyncio.sleep(0)


async def main() -> None:
    """Run pubsub loop."""
    await cache.set("foo1", "bar1FFFF567")
    print(await cache.get("foo1"))
    pubsub = cache.pubsub()
    await pubsub.subscribe("channel:1", "channel:2")

    consumer_future = asyncio.create_task(consumer(pubsub))

    await cache.publish("channel:1", "Hello")
    await cache.publish("channel:2", "World")
    await cache.publish("channel:1", STOPWORD)

    await asyncio.wait([consumer_future])


if __name__ == "__main__":
    asyncio.run(main())
