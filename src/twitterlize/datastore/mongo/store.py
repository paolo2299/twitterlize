from twitterlize.settings import MongoStores
from twitterlize.cache import CacheType
from twitterlize.cache.rediscache import RedisCache
from twitterlize.cache.memcache_cli import Memcache
from twitterlize.datastore.mongo.factory import MongoFactory

#TODO implement locking for to make cache updates atomic

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
        cache_namespace = storeconf.get("cache_namespace")
        cachesecs = storeconf.get("cachesecs")
        # create the cache
        if cachetype == CacheType.Off:
            self._cache = None
        elif cachetype == CacheType.Volatile:
            self._cache = Memcache(namespace=cache_namespace)
        elif cachetype == CacheType.Persistent:
            self._cache = RedisCache(cachesecs=cachesecs, namespace=cache_namespace)
        else:
            raise Exception("Unknown cache type enumeration %s" % cachetype)

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
        return result

    def save(self, doc):
        key = self.store.save(doc)
        self._set_cache(key, doc)
        return key

    def find(self, query=None, fields=None):
        query = query or {}
        if fields:
            cursor = self.store.find(query, fields)
        else:
            cursor = self.store.find(query)
        return cursor

    def count(self):
        return self.store.count()

    def update(self, query, update_dict, upsert=False):
        self.store.update(query, update_dict, upsert=upsert)
        if self._cache:
            new_doc = self.store.find_one(query)
            key = new_doc["_id"]
            self._set_cache(key, new_doc)
            
    def delete_one(self, key):
        self.store.remove({"_id": key})
        if self._cache:
            self._cache.delete(key)
        