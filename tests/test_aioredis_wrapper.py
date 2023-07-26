import logging
from typing import Awaitable
from unittest.mock import Mock, patch

import pytest
from redis import asyncio as aioredis

from redis_redirect import aioredis_wrapper

log = logging.getLogger(__name__)


async def async_get(result):
    return result


class RedisMock:
    """If inited with host=`redirect-host` then raise MOVED exception with redirect to `fake-host:0`"""

    def __init__(self, host, port, db):
        self.host = host
        self.connection = Mock()
        self.connection_pool = Mock()
        self._DEL_MESSAGE = Mock()

    def get(self, key) -> Awaitable:
        log.debug(f"RedisMock.get ({self.host})")
        if self.host == "redirect-host":
            raise aioredis.ResponseError("MOVED ?? fake-host:0")
        return async_get("fake_value")


@pytest.mark.asyncio
async def test_aiocache_no_redirect():
    with patch("redis_redirect.aioredis_wrapper.aioredis.Redis", RedisMock):
        aioredis.from_url = Mock(return_value=RedisMock(host="fake-host", port=0, db=0))
        wrapper = aioredis_wrapper.AioRedisWrapper(host="fake-host", port=0)
        assert await wrapper.get("key") == "fake_value"
        aioredis.from_url.assert_called_once()


@pytest.mark.asyncio
async def test_aiocache_with_redirect():
    with patch("redis_redirect.aioredis_wrapper.aioredis.Redis", RedisMock):
        aioredis.from_url = Mock(return_value=RedisMock(host="redirect-host", port=0, db=0))
        wrapper = aioredis_wrapper.AioRedisWrapper(host="redirect-host", port=0)
        aioredis.from_url.assert_called_once()
        aioredis.from_url.reset_mock()
        aioredis.from_url = Mock(return_value=RedisMock(host="fake-host", port=0, db=0))
        assert await wrapper.get("key") == "fake_value"
        aioredis.from_url.assert_called_with("redis://fake-host")
