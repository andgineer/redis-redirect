[![Build Status](https://github.com/andgineer/redis-redirect/workflows/ci/badge.svg)](https://github.com/andgineer/redis-redirect/actions)
[![Coverage](https://raw.githubusercontent.com/andgineer/redis-redirect/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/redis-redirect/blob/python-coverage-comment-action-data/htmlcov/index.html)
# (aio)REDIS wrapper to deal with cluster redirect exceptions `MOVED`

Handles exceptions like:

        redis.exceptions.ResponseError: MOVED 4085 10.213.192.152:6379

When Redis returns a MOVED exception, it indicates that the client should repeat its request for the specified host.

This exception can occur in the following situations:

1. Your Redis configuration is incorrect. In this case, you should fix your Redis settings.
   `redis-redirect` cannot help in this scenario.
2. You are connecting to the wrong host.
   For instance, if you're using Amazon managed Redis (ElastiCache), Amazon provides a fixed
   DNS name for the configuration node and an IP address for the work node. The IP address may change in the future.
   In such cases, you should use the DNS name. `redis-redirect` cannot help in this scenario.
3. You're using a multi-node Redis cluster.
   In this case, you can use `redis-redirect` to automatically switch between Redis nodes or shards.

`redis-redirect` handles `MOVED` exceptions seamlessly and transparently.

# Installation

        pip install redis-redirect

# Usage

        import redis_redirect

        redis = redis_redirect.Redis(host='my-redis.com', port=6379, db=0)
        redis.set('foo', 'bar')


# How it works

`redis-redirect` transparently handles Redis server redirection exceptions.

When a client sends a request to the Redis server, `redis-redirect` checks if
the server has returned a `MOVED` exception.

If a `MOVED` exception is received, `redis-redirect` updates the Redis server address and resends
the request to the new address.

After updating the Redis server address, `redis-redirect` transparently forwards subsequent requests to
the new Redis server address.

## Coverage report
* [Codecov](https://app.codecov.io/gh/andgineer/redis-redirect/tree/master/src%2Fredis_redirect)
* [Coveralls](https://coveralls.io/github/andgineer/redis-redirect)
