from twitterlize import settings
from twitterlize.cache import Cache
from twitterlize.utils import serialize, deserialize #TODO

#TODO - check memcache commands are correct

class Memcache(Cache):
    def __init__(self):
        self._memcache = None
	self._namespace = settings.Memcache["namespace"]

    @property
    def memcache(self):
        if not self._memcache:
	    self._memcache = MemcacheFactory.getconn()
	return self._memcache

    def put(self, key, val):
        key = self._namespace + key
        return self.memcache.put(key, serialize(val))

    def get(self, key):
        key = self._namespace + key
        val = self.memcache.get(key)
	if val == "X":
	    return None
	if val:
	    val = deserialize(val)
	return val

    def delete(self, key):
        key = self._namespace + key
        return self.memcache.put(key, "X")


class MemcacheFactory(object):

    _memcache = None

    @classmethod
    def getconn(cls):
        """Return cached connection if it exists.
        Otherwise, create a new connection and cache it.

        """
        if not cls._memcache:
            memcacheconf = settings.Memcache
            cls._memcache = Memcache(memcacheconf["host"], memcacheconf["port"])
        return cls._memcache
