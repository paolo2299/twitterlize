from twitterlize.cache import Cache
from twitterlize import settings
from twitterlize.datastore.redis.factory import RedisFactory
from twitterlize.utils import serialize, deserialize

        
class RedisCache(Cache):
    def __init__(self, cachesecs=0, namespace=None):
        self._redis = None
        self._cachesecs = cachesecs
        self._namespace = namespace or ""

    @property
    def redis(self):
        if not self._redis:
            self._redis = RedisFactory.getconn()
        return self._redis

    def put(self, key, val, expire=None):
        key = self._namespace + key
        result = self.redis.set(key, serialize(val))
        expire = expire or self._cachesecs
        if expire:
            self.expire(key, expire)
        return result

    def get(self, key, expire=None):
        key = self._namespace + key
        val = self.redis.get(key)
        if val:
            val = deserialize(val)
            expire = expire or self._cachesecs
            if expire:
                self.expire(key, expire)
        return val

    def expire(self, key, secs):
        key = self._namespace + key
        return self.redis.expire(key, secs)

    def delete(self, key):
        key = self._namespace + key
        return self.redis.delete(key)

