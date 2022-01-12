import redis as redis

from dataengine.config import REDIS_HOST, REDIS_PORT

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)


def get_redis_client() -> redis.Redis:
    return redis.Redis(connection_pool=pool)
