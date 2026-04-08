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

    some_attr = "attr_value"

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

    def error_get(self, key) -> Awaitable:
        raise aioredis.ResponseError("ERR some other error")


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


@pytest.mark.asyncio
async def test_aio_non_moved_error_is_reraised():
    with patch("redis_redirect.aioredis_wrapper.aioredis.Redis", RedisMock):
        aioredis.from_url = Mock(return_value=RedisMock(host="fake-host", port=0, db=0))
        wrapper = aioredis_wrapper.AioRedisWrapper(host="fake-host", port=0)
        try:
            await wrapper.error_get("key")
            assert False, "Expected ResponseError"
        except aioredis.ResponseError as e:
            assert "ERR some other error" in str(e)


def test_aio_non_awaitable_attribute_passthrough():
    with patch("redis_redirect.aioredis_wrapper.aioredis.Redis", RedisMock):
        aioredis.from_url = Mock(return_value=RedisMock(host="fake-host", port=0, db=0))
        wrapper = aioredis_wrapper.AioRedisWrapper(host="fake-host", port=0)
        assert wrapper.some_attr == "attr_value"


def test_aio_wrapper_own_attributes():
    with patch("redis_redirect.aioredis_wrapper.aioredis.Redis", RedisMock):
        aioredis.from_url = Mock(return_value=RedisMock(host="fake-host", port=0, db=0))
        wrapper = aioredis_wrapper.AioRedisWrapper(host="fake-host", port=1234, db=2)
        assert wrapper._host == "fake-host"
        assert wrapper._port == 1234
        assert wrapper._db == 2
