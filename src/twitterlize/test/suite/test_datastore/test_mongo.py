from twitterlize.test.framework import fixture
from twitterlize.test.framework.mongo import Mongo
from twitterlize.test.framework.redis import Redis
from twitterlize.test.framework.memcache import Memcache
from twitterlize.datastore.mongo.store import MongoStore
from twitterlize.cache import CacheType
from twitterlize.utils import serialize
import unittest
from twitterlize import settings


class MongoStoreTest(unittest.TestCase):
    
    def setUp(self):
        fixture.setup_database_settings()
        self._redis = Redis()
        self._mongo = Mongo("unittest")
        self._memcache = Memcache()
        self._redis.clear()
        self._mongo.clear()
        self._memcache.put("unittest:test", "X")

    def test_no_cache(self):
        store = MongoStore("unittest")
        actual = store.save({"_id": "test", "hello": "world"})
        expected = "test"
        self.assertEqual(expected, actual)
        
        actual = store.find_one("test")
        expected = {"_id": "test", "hello": "world"}
        self.assertEqual(expected, actual)
        
        store.save({"_id": "test2", "goodbye": "world"})
        
        actual = list(store.find({}))
        expected = [
            {"_id": "test", "hello": "world"},
            {"_id": "test2", "goodbye": "world"}
        ]
        self.assertEqual(expected, actual)

        actual = list(store.find({"goodbye": {"$exists": True}}))
        expected = [{"_id": "test2", "goodbye": "world"}]
        self.assertEqual(expected, actual)
        
        actual = list(store.find().limit(1))
        expected = [{"_id": "test", "hello": "world"}]
        self.assertEqual(expected, actual)
        
        actual = store.count()
        self.assertEqual(2, actual)
        
        store.delete_one("test")
        actual = list(store.find())
        expected = [{"_id": "test2", "goodbye": "world"}]
        
        store.update({"_id": "test2"}, {"$set":{"goodbye": "universe"}})
        actual = store.find_one("test2")
        expected = {"_id": "test2", "goodbye": "universe"}
        self.assertEqual(expected, actual)
        
        store.update({"_id": "test3"}, {"$set":{"goodbye": "multiverse"}}, upsert=True)
        actual = store.find_one("test3")
        expected = {"_id": "test3", "goodbye": "multiverse"}
        self.assertEqual(expected, actual)
        
    def test_redis_cache(self):
        settings.MongoStores["unittest"]["cachetype"] = CacheType.Persistent
        store = MongoStore("unittest")
        
        store.save({"_id": "test", "hello": "world"})
        actual = self._mongo.find_one("test")
        self.assertEqual({"_id": "test", "hello": "world"}, actual)
        
        actual = self._redis.get("unittest:test")
        expected = serialize({"_id": "test", "hello": "world"})
        self.assertEqual(expected, actual)
        
        self._mongo.delete_one("test")
        actual = self._mongo.find_one("test")
        self.assertEqual(None, actual)
        
        actual = store.find_one("test")
        self.assertEqual({"_id": "test", "hello": "world"}, actual)
        
        store.save({"_id": "test", "hello": "world"})
        store.update({"_id": "test"}, {"$set":{"hello": "universe"}})
        actual = self._redis.get("unittest:test")
        expected = serialize({"_id": "test", "hello": "universe"})
        self.assertEqual(expected, actual)
        
        store.delete_one("test")
        actual = store.find_one("test")
        self.assertEqual(None, actual)
        actual = self._redis.get("unittest:test")
        self.assertEqual(None, actual)
        
    def test_memcache_cache(self):
        settings.MongoStores["unittest"]["cachetype"] = CacheType.Volatile
        store = MongoStore("unittest")
        
        actual = self._memcache.get("unittest:test")
        self.assertEqual("X", actual)
        
        store.save({"_id": "test", "hello": "world"})
        actual = self._mongo.find_one("test")
        self.assertEqual({"_id": "test", "hello": "world"}, actual)
        
        actual = self._memcache.get("unittest:test")
        expected = serialize({"_id": "test", "hello": "world"})
        self.assertEqual(expected, actual)
        
        self._mongo.delete_one("test")
        actual = self._mongo.find_one("test")
        self.assertEqual(None, actual)
        
        actual = store.find_one("test")
        self.assertEqual({"_id": "test", "hello": "world"}, actual)
        
        store.save({"_id": "test", "hello": "world"})
        store.update({"_id": "test"}, {"$set":{"hello": "universe"}})
        actual = self._memcache.get("unittest:test")
        expected = serialize({"_id": "test", "hello": "universe"})
        self.assertEqual(expected, actual)
        
        store.delete_one("test")
        actual = store.find_one("test")
        self.assertEqual(None, actual)
        actual = self._memcache.get("unittest:test")
        self.assertEqual("X", actual)
        
    
if __name__ == "__main__":
    fixture.setup()
    unittest.main()