from twitterlize.test.framework import fixture
from twitterlize.test.framework.mongo import Mongo
from twitterlize.test.framework.redis import Redis
from twitterlize.datastore.mongo.store import MongoStore
import unittest
import time


class MongoStoreTest(unittest.TestCase):
    
    def setUp(self):
        self._redis = Redis()
        self._mongo = Mongo("unittest")

    def test_no_cache(self):
        store = MongoStore("unittest")
        
        
if __name__ == "__main__":
    fixture.setup()
    unittest.main()