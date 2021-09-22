import asyncio
import inspect
from typing import Awaitable

import aioredis
import aioredis.exceptions

REDIS_CLUSTER_CONFIG_HOST = "???.cache.amazonaws.com"
REDIS_CLUSTER_CONFIG_PORT = 6379


class AioRedisWrapper:
    """
    Wraps all Redis methods to catch "MOVED" exception.
    Change host&port if any and repeat the method call.

    todo make autocomplete work (inherit from aioredis and use __get_attribute__ ?)
    """

    _wrapped_attrs = []

    def __init__(self, host: str, port: int, db: int = 0):
        self._host = host
        self._port = port
        self._db = db
        self.original_redis = aioredis.from_url(
            f"redis://{self._host}"
        )  # todo use port=self._port

    def __getattr__(self, attr_name):
        attr = getattr(self.original_redis, attr_name)
        if inspect.signature(attr).return_annotation == Awaitable:

            async def wrapper(*args, **kwargs):
                nonlocal attr
                try:
                    result_future = asyncio.gather(
                        attr(*args, **kwargs)
                    )  # do not use await - we should propagate exception
                    return await result_future
                except aioredis.exceptions.ResponseError as e:
                    if e.args[0].startswith(
                        "MOVED"
                    ):  # something like "MOVED 12182 10.188.32.41:6379"
                        # For some reasons even a Redis Cluster with one node can redirect requests
                        # We use the redirect address as new Redis master and hope the cluster have only one node so no more MOVED
                        redis_connection_str = e.args[0].split(" ")[2]
                        self._host, self._port = redis_connection_str.split(":")
                        print(f"Redis redirect to node {self._host}:{self._port}")
                        self.original_redis = aioredis.from_url(
                            f"redis://{self._host}"
                        )  # todo use port=self._port
                        for attr_name_to_delete in self._wrapped_attrs:
                            delattr(self, attr_name_to_delete)
                        self._wrapped_attrs.clear()
                        attr = getattr(self.original_redis, attr_name)
                        result_future = asyncio.gather(
                            attr(*args, **kwargs)
                        )  # do not use await - we should propagate exception
                        return await result_future
                raise RuntimeError(f"Cannot access cluster {self._host}:{self._port}")

            setattr(
                self, attr_name, wrapper
            )  # next time AioRedisWrapper attr will be used without __get__attr call
            self._wrapped_attrs.append(attr_name)
            return wrapper
        return attr


cache = AioRedisWrapper(host=REDIS_CLUSTER_CONFIG_HOST, port=REDIS_CLUSTER_CONFIG_PORT)


if __name__ == "__main__":
    cache.set("foo1", "bar191234567")
    print(cache.get("foo"))
