import redis
from redis import TimeoutError


class CacheObject:

    def __init__(self, connect, key):
        """
        redis存储的格式为:
        {"key":{"field":"value"}}
        :param connect:object
        :param key:字段名
        """
        self.redis = redis.Redis(connection_pool=connect.pool, decode_responses=True)

        try:
            self.redis.ping()
        except TimeoutError as e:
            raise e
        self.key=key

    def expire(self, time):
        self.redis.expire(name=self.key, time=time)

    def delete(self):
        self.redis.delete(self.key)

    @staticmethod
    def decode(value):
        if value:
            return value.decode('utf-8')


class CacheDict(CacheObject):
    def __init__(self, connect, key):
        super(CacheDict, self).__init__(connect, key)

    def __getitem__(self, field):
        return CacheObject.decode(self.redis.hget(self.key, field))

    def __setitem__(self, field, value):
        """
        :param key:
        :param value:
        :return:
        """
        self.redis.hset(name=self.key, key=field, value=value)
