from twitterlize.cache.rediscache import RedisFactory

class Redis(object):
    def __init__(self):
        self._redis = None

    @property
    def redis(self):
        if not self._redis:
            self._redis = RedisFactory.getconn()
        return self._redis

    def put(self, key, val):
        return self.redis.set(key, val)

    def get(self, key):
        return self.redis.get(key)

    def delete_key(self, key):
        return self.redis.delete(key)

    def delete_pattern(self, pattern):
        #TODO
        pass
    