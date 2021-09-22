(aio)REDIS wrapper to deal with cluster redirect exceptions like

        redis.exceptions.ResponseError: MOVED 4085 10.213.192.152:6379

With this exception REDIS say that you should repeat your request for
the specified host.

That happens
1) your REDIS configuration just wrong
2) you connect to thw wrong host
3) you are using multi-node REDIS cluster - you should use my wrapper

First case is simple - just check your settings.

Second case could happen if for example you are using Amazon managed REDIS (elastic cache)
so you have some fixed DNS name for configuration node, and just an IP
for the work node, and this IP can change in the future.
So you want to use this fixed DNS name.

And for the third case you definitely need my wrapper to automatically switch between
REDIS nodes.

My wrapper will catch the "MOVED" exception and change REDIS address
according to the address in the exception.
