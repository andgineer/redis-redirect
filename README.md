[![Build Status](https://github.com/andgineer/redis-redirect//workflows/ci/badge.svg)](https://github.com/andgineer/redis-redirect//actions)

# (aio)REDIS wrapper to deal with cluster redirect exceptions `MOVED`

Like

        redis.exceptions.ResponseError: MOVED 4085 10.213.192.152:6379

With this exception REDIS tells that you should repeat your request for
the specified host.

That happens
1) your REDIS configuration just wrong
2) you connect to the wrong host
3) you are using multi-node REDIS cluster

First case is just configuration error. Fix your settings, for sure the wrapper won't help you.

Second case could happen if for example you are using Amazon managed REDIS (elastic cache)
for which Amazon provides fixed DNS name for configuration node, and just an IP
for the work node. The IP can change in the future.
So you better use this fixed DNS name, but it cannot process requests and will
redirect you to the work node.

For the third case you could use the wrapper to automatically switch between
REDIS nodes (shards of you REDIS data).

# Installation

        pip install redis-redirect

# Usage
    
        import redis_redirect

        redis = redis_redirect.Redis(host='my-redis.com', port=6379, db=0)
        redis.set('foo', 'bar')


# How it works

If no `MOVED` exception happened, the wrapper transparent and change nothing, just pass all the requests
to the internal wrapped Redis.

If the wrapped Redis redirect to another host, the wrapper will catch the `MOVED` exception 
and change wrapped Redis address according to the address in the `MOVED` exception.

Next the wrapper automatically repeat the same request now with wrapped Redis pointing
to the new host.

After the redirect and changing wrapped Redis, the wrapper will be transparent again 
and won't affect the performance.
