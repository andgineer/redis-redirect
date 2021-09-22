(aio)REDIS wrapper to deal with cluster redirect exceptions like

        redis.exceptions.ResponseError: MOVED 4085 10.213.192.152:6379

With this exception REDIS say that you should repeat your request for
the specified host.

That happens
1) your REDIS configuration just wrong
2) you connect to the wrong host
3) you are using multi-node REDIS cluster - you should use my wrapper

First case is simple - just check your settings.

Second case could happen if for example you are using Amazon managed REDIS (elastic cache)
for which Amazon provides fixed DNS name for configuration node, and just an IP
for the work node. The IP can change in the future.
So you better use this fixed DNS name, but it cannot process requests and will
redirect you to the work node.

And for the third case you could use my wrapper to automatically switch between
REDIS nodes (shards of you REDIS data).

My wrapper catch the "MOVED" exception and change REDIS address
according to the address in the exception.

It just proxy all the REDIS methods.
In this early version it is doing that dynamically, so code autocomplete won't work, sorry.