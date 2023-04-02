from redis_redirect import aioredis_wrapper
import aioredis
import aioredis.exceptions
import pytest
import logging
from unittest.mock import Mock, patch
from typing import Awaitable


log = logging.getLogger(__name__)


async def async_get(result):
    return result


class RedisMock:
    def __init__(self, host, port, db):
        self.host = host
        self.connection = Mock()
        self.connection_pool = Mock()
        self._DEL_MESSAGE = Mock()

    def get(self, key) -> Awaitable:
        log.debug(f"RedisMock.get ({self.host})")
        if self.host == "redirect-host":
            raise aioredis.exceptions.ResponseError("MOVED ?? fake-host:0")
        return async_get("fake_value")


@pytest.mark.asyncio
async def test_aiocache():
    aioredis.Redis = RedisMock
    aioredis.from_url = Mock(return_value=RedisMock(host="fake-host", port=0, db=0))
    wrapper = aioredis_wrapper.AioRedisWrapper(host="fake-host", port=0)
    assert await wrapper.get("key") == "fake_value"
    aioredis.from_url.assert_called_once()

    aioredis.from_url = Mock(return_value=RedisMock(host="redirect-host", port=0, db=0))
    wrapper = aioredis_wrapper.AioRedisWrapper(host="redirect-host", port=0)
    aioredis.from_url.assert_called_once()
    aioredis.from_url = Mock(return_value=RedisMock(host="fake-host", port=0, db=0))
    assert await wrapper.get("key") == "fake_value"
    aioredis.from_url.assert_called_with("redis://fake-host")

