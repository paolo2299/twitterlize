from twitterlize.datastore.mongo.factory import MongoFactory


class Mongo(object):

    def __init__(self, storeid):
        self._store = None
        self._store_id = storeid

    @property
    def store(self):
        if not self._store:
            self._store = MongoFactory.getconn(self.store_id)
        return self._store

    def find_one(self, key):
        return self.store.find_one(key)

    def save(self, doc):
        return self.store.save(doc)

    def find(self, query):
        """We don't look in the cache for complex queries or
        scans.
        """
        return self.store.find(query)

    def count(self, query=None):
        query = query or {}
        return self.store.count(query)

