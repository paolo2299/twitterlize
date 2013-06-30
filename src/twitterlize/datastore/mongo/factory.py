from pymongo import Connection
from twitterlize.settings import MongoStores

class MongoFactory(object):

    _collections = {}

    @classmethod
    def getconn(cls, storeid):
        """Return cached connection if it exists.
	Otherwise, create a new connection and cache it.

	"""
        try:
            storeconf = MongoStores[storeid]
        except KeyError:
            raise Exception("Requested non-existent store %s" % storeid)
        # Check for a cached connection for this collection
        db = cls._get_db_name(storeconf)
        coll = storeconf["collection"]
        cachekey = cls._cachekey(db, coll)
        collection = cls._collections.get(cachekey)
        if collection:
            return collection
        # No cached connection exists so create a new one
        conn = Connection(storeconf["host"], storeconf["port"])
        collection = conn[db][coll]
        cls._collections[cachekey] = collection
        return collection

    @classmethod
    def clean_up(cls):
        for coll in cls._collections.values():
            coll.end_request()

    @staticmethod
    def _cachekey(db, collection):
        return ":".join([db, collection])

