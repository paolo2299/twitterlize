from twitterlize.test.framework import fixture
from twitterlize.test.framework.mongo import Mongo
from twitterlize.utils import serialize
import unittest
from twitterlize import settings
from twotterlize.datastore.countstore import CountStore


class CountStoreTest(unittest.TestCase):
    
    def setUp(self):
        fixture.setup_database_settings()
        self._mongo = Mongo("unittest")
        self._mongo.clear()

    def test_put_no_total_count(self):
        countstore = CountStore()
        
    
if __name__ == "__main__":
    fixture.setup()
    unittest.main()
