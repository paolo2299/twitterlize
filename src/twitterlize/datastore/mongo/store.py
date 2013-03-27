from twitterlize.settings import MongoStores
from twitterlize.cache import CacheType
from twitterlize.cache.redis import RedisCache
from twitterlize.cache.memcache import Memcache
from twitterlize.datastore.mongo.factory import MongoFactory

class MongoStore(object):
    """Wrapper around mongo access that handles caching."""

    def __init__(self, storeid):
        """Args:
	       storeid - ID from settings.py MongoStores config.

	"""
        self._store = None
	self._storeid = storeid
	try:
	    storeconf = MongoStores[storeid]
	except KeyError:
	    raise Exception("Unrecognized store ID: %s" % storeid)
	cachetype = storeconf["cachetype"]
	cachesecs = storeconf.get("cachesecs")
	# create the cache
	if cachetype == CacheType.Off:
	    self._cache = None
	elif cachetype == CacheType.Volatile:
	    self._cache = Memcache()
	elif cachetype == CacheType.Persistent:
	    if cachesecs:
	        self._cache = RedisCache(cachesecs)
	    else:
	        self._cache = RedisCache()
	else:
	    raise Exception("Unknown cachetype enumeration %s" % cachetype)

    @property
    def store(self):
        if not self._store:
	    self._store = MongoFactory.getconn(self._storeid)
	return self._store

    def _get_cached(self, key):
        if self._cache:
	    return self._cache.get(key)
	return None

    def _set_cache(self, key, val):
        if self._cache:
	    self._cache.put(key, val)

    def find_one(self, key):
        result = self._get_cached(key)
	if result:
	    return result
        result = self.store.find_one(key)
	self._set_cache(key, result)
	return result

    def save(self, doc):
        key = self.store.save(doc)
	self._set_cache(key, doc)
	return key

    def find(self, query, fields=None):
        """We don't look in the cache for complex queries or
	scans."""
	if fields:
	    return self.store.find(query, fields)
	else:
	    return self.store.find(query)

    def count(self, query=None):
        query = query or {}
	return self.store.count(query)

    def update(self, query, update_dict, upsert=False):
        #No sensible way to use atomic updates with caching
	#We would have to implement our own 
	#lock-fetch-save-unlock
	#no need to do this for now
        if self._cache:
	    raise Exception("Tried to perform an update on a MongoStore\
	                     with a cache. This is not allowed.")
	self.store.update(query, update_dict, upsert=upsert)
