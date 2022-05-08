import logging
import redis
from datetime import timedelta

from paraphrasing_bot.src.services.Config import Config


class Redis:
    def __init__(self):
        self.app_config = Config()
        self.logging = logging.getLogger("redis-service")

        self.connection = redis.Redis(
            host=self.app_config.REDIS_HOST,
            port=self.app_config.REDIS_PORT,
            password=self.app_config.REDIS_PASSWORD,
            db=self.app_config.REDIS_DATABASE,
            decode_responses=True,
            health_check_interval=10
        )

    def save(self, key: str, value: str, ttl: timedelta = None, raise_exception: bool = False):
        if not ttl or not isinstance(ttl, timedelta):
            ttl = timedelta(seconds=self.app_config.REDIS_DEFAULT_TTL)

        try:
            self.connection.set(name=key, value=value, ex=ttl)
        except redis.ConnectionError as e:
            self.logging.error(e)

            if raise_exception:
                raise e

    def get(self, key: str, raise_exception: bool = False):
        try:
            self.connection.get(name=key)
        except redis.ConnectionError as e:
            self.logging.error(e)

            if raise_exception:
                raise e
