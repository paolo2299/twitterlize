from twitterlize.test.framework import fixture
from twitterlize.test.framework.redis import Redis
from twitterlize.cache.rediscache import RedisCache
import unittest
import time


class RedisCacheTest(unittest.TestCase):
    
    def setUp(self):
        self._redis = Redis()
        self._redis.clear()

    def test_put_and_get_no_namespace(self):
        cache = RedisCache()
        cache.put("unittestkey1", "val1")
        actual = self._redis.get("unittestkey1")
        expected = "val1"
        self.assertEqual(expected, actual)
        
        actual = cache.get("unittestkey1")
        expected = "val1"
        self.assertEqual(expected, actual)

    def test_put_and_get_with_namespace(self):
        cache = RedisCache(namespace="unittest:")
        cache.put("key1", "val1")
        actual = self._redis.get("unittest:key1")
        expected = "val1"
        self.assertEqual(expected, actual)
        
        actual = self._redis.get("key1")
        expected = None
        self.assertEqual(expected, actual)
        
        actual = cache.get("key1")
        expected = "val1"
        self.assertEqual(expected, actual)
        
    def test_delete(self):
        cache = RedisCache(namespace="unittest:")
        cache.put("key1", "val1")
        actual = cache.get("key1")
        expected = "val1"
        self.assertEqual(expected, actual)
        
        cache.delete("key1")
        actual = cache.get("key1")
        expected = None
        self.assertEqual(expected, actual)

    def test_expire(self):
        cache = RedisCache(namespace="unittest:")
        cache.put("key1", "val1")
        actual = cache.get("key1")
        expected = "val1"
        self.assertEqual(expected, actual)
        
        cache.expire("key1", 2)
        time.sleep(1)
        
        actual = cache.get("key1")
        expected = "val1"
        self.assertEqual(expected, actual)
        
        time.sleep(1.5)
        
        actual = cache.get("key1")
        expected = None
        self.assertEqual(expected, actual)
        
    def test_setting_cachesecs(self):
        cache = RedisCache(namespace="unittest:", cachesecs=2)
        cache.put("key1", "val1")
        time.sleep(1)
        
        actual = cache.get("key1")
        expected = "val1"
        self.assertEqual(expected, actual)
        
        time.sleep(1.5)
        
        actual = cache.get("key1")
        expected = None
        self.assertEqual(expected, actual)
        
    def test_non_string_storage(self):
        cache = RedisCache(namespace="unittest:")
        cache.put("key1", {"hello": "world"})
        actual = cache.get("key1")
        expected = {"hello": "world"}
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    fixture.setup()
    unittest.main()