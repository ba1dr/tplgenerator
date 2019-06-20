
import redis
import aioredis

from django.conf import settings

globalclient = {}
_pools = {}


async def get_redis_conn(loop, redis_url=None):
    global _pools
    redis_url = redis_url or settings.REDIS_URL
    if redis_url not in _pools:
        redis = await aioredis.create_redis_pool(
            redis_url,
            minsize=1, maxsize=3,
            loop=loop)
        _pools[redis_url] = redis
    return _pools[redis_url]


def create_global_client(redis_url=None):
    global globalclient
    redis_url = redis_url or settings.SEMAPHORES_REDIS_URL
    if redis_url not in globalclient:
        globalclient[redis_url] = redis.StrictRedis.from_url(redis_url)
    # print("globalclient", id(globalclient))
    return globalclient[redis_url]
