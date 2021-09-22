import redis
import redis.exceptions

REDIS_CLUSTER_CONFIG_HOST = "???.cache.amazonaws.com"
REDIS_CLUSTER_CONFIG_PORT = 6379


class RedisWrapper:
    """
    Wraps all Redis methods to catch "MOVED" exception.
    Change host&port if any and repeat the method call.
    """

    _wrapped_attrs = []

    def __init__(self, host: str, port: int, db: int = 0):
        self._host = host
        self._port = port
        self._db = db
        self._original_redis = redis.Redis(host=self._host, port=self._port, db=self._db)

    def __getattr__(self, attr_name):
        attr = getattr(self._original_redis, attr_name)
        if hasattr(attr, "__call__"):

            def wrapper(*args, **kwargs):
                nonlocal attr
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
                        print(f"Redis redirect to node {self._host}:{self._port}")
                        self._original_redis = redis.Redis(
                            host=self._host, port=self._port, db=self._db
                        )
                        for attr_name_to_delete in self._wrapped_attrs:
                            delattr(self, attr_name_to_delete)
                        self._wrapped_attrs.clear()
                        attr = getattr(self._original_redis, attr_name)
                        return attr(*args, **kwargs)
                raise RuntimeError(f"Cannot access cluster {self._host}:{self._port}")

            setattr(
                self, attr_name, wrapper
            )  # next time RedisWrapper attr will be used without __get__attr call
            self._wrapped_attrs.append(attr_name)
            return wrapper
        return attr


cache = RedisWrapper(
    host=REDIS_CLUSTER_CONFIG_HOST,
    port=REDIS_CLUSTER_CONFIG_PORT,
)


if __name__ == "__main__":
    cache.set("foo1", "bar191234567")
    print(cache.get("foo"))
