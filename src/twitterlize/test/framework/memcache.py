from twitterlize.cache.memcache_cli import MemcacheFactory

class Memcache(object):
    def __init__(self):
        self._cache = None

    @property
    def cache(self):
        if not self._cache:
            self._cache = MemcacheFactory.getconn()
        return self._cache

    def put(self, key, val):
        return self.cache.set(key, val)

    def get(self, key):
        return self.cache.get(key)

    