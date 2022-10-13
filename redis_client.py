import redis

REDIS_HOST = "airflow_redis"
REDIS_PORT = 6379


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
        )

    def set(self, key, value):
        self.client.set(name=key, value=value)

    def get(self, key):
        return self.client.get(name=key)
