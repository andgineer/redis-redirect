import redis
import redis.exceptions
import os
import logging

REDIS_HOST = os.getenv("REDIS_HOST", "???.cache.amazonaws.com")
REDIS_PORT = 6379

log = logging.getLogger(__name__)


class RedisWrapper(redis.Redis):
    """
    Wraps all Redis methods to catch "MOVED" exception.
    Change host&port if any and repeat the method call.
    """
    _original_redis = None

    def __init__(self, host: str, port: int, db: int = 0):  # pylint: disable=super-init-not-called
        # we inherit only for code completion in IDE so no need to init parent
        self._host = host
        self._port = port
        self._db = db
        self._original_redis = redis.Redis(host=self._host, port=self._port, db=self._db)

    def __getattribute__(self, attr_name):
        # todo place upstream Redis attributes to __dict__ for IDE autocomplete works
        original_redis = object.__getattribute__(self, "_original_redis")  # to prevent __getattribute__ recursion
        try:
            attr = object.__getattribute__(original_redis, attr_name)
        except AttributeError:
            if attr_name not in object.__getattribute__(self, "__dict__"):  # to prevent __getattribute__ recursion
                raise  # this is not RedisWrapper attribute
            return object.__getattribute__(self, attr_name)  # RedisWrapper own attribute
        if hasattr(attr, "__call__"):

            def wrapper(*args, **kwargs):
                nonlocal attr
                log.debug(f"wrapped {attr_name} call")
                try:
                    return attr(*args, **kwargs)
                except redis.exceptions.ResponseError as e:
                    if e.args[0].startswith(
                        "MOVED"
                    ):  # something like "MOVED 12182 10.188.32.41:6379"
                        # For some reasons even a Redis Cluster with one node can redirect requests
                        # We use the redirect address as new Redis master and hope the cluster have only one node so no more MOVED
                        redis_connection_str = e.args[0].split(" ")[2]
                        self._host, self._port = redis_connection_str.split(":")
                        log.debug(f"Redis redirect to node {self._host}:{self._port}")
                        original_redis = redis.Redis(
                            host=self._host, port=self._port, db=self._db
                        )
                        self._original_redis = original_redis
                        attr = getattr(original_redis, attr_name)
                        return attr(*args, **kwargs)
                    raise

            log.debug(f"Wrapping {attr_name}")
            return wrapper
        return attr


cache = RedisWrapper(
    host=REDIS_HOST,
    port=REDIS_PORT,
)


if __name__ == "__main__":
    cache.set("foo1", "bar191234567")
    print(cache.get("foo"))
