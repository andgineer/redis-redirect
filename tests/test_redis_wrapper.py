import logging
from unittest.mock import patch

import redis
import redis.exceptions

from redis_redirect import redis_wrapper

log = logging.getLogger(__name__)


class RedisMock:
    def __init__(self, host, port, db):
        self.host = host

    def get(self, key):
        log.debug(f"RedisMock.get ({self.host})")
        if self.host == "redirect-host":
            raise redis.exceptions.ResponseError("MOVED ?? fake-host:0")
        return "fake_value"

    def close(self, *args, **kwargs):
        """
        Redis call the method after any request so we need something to wrap
        """
        log.debug(f"RedisMock.close ({self.host})")


def test_cache_no_redirect():
    with patch("redis_redirect.redis_wrapper.redis.Redis", RedisMock):
        wrapper = redis_wrapper.RedisWrapper(host="-fake-host-", port=0)
        assert wrapper.get("key") == "fake_value"
        assert wrapper._original_redis.host == "-fake-host-"


def test_cache_with_redirect():
    with patch("redis_redirect.redis_wrapper.redis.Redis", RedisMock):
        wrapper = redis_wrapper.RedisWrapper(host="redirect-host", port=0)
        assert wrapper.get("key") == "fake_value"
        assert wrapper._original_redis.host == "fake-host"
