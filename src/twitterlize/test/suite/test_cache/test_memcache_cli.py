from twitterlize.test.framework import fixture
from twitterlize.test.framework.memcache import Memcache as TestMemcache
from twitterlize.cache.memcache_cli import Memcache
import unittest


class MemcacheTest(unittest.TestCase):
    
    def setUp(self):
        self._memcache = TestMemcache()
        self._memcache.put("unittestkey1", "X")
        self._memcache.put("unittest:key1", "X")

    def test_put_and_get_no_namespace(self):
        cache = Memcache()
        cache.put("unittestkey1", "val1")
        actual = self._memcache.get("unittestkey1")
        expected = "val1"
        self.assertEqual(expected, actual)
        
        actual = cache.get("unittestkey1")
        expected = "val1"
        self.assertEqual(expected, actual)

    def test_put_and_get_with_namespace(self):
        cache = Memcache(namespace="unittest:")
        cache.put("key1", "val1")
        actual = self._memcache.get("unittest:key1")
        expected = "val1"
        self.assertEqual(expected, actual)
        
        actual = self._memcache.get("key1")
        expected = None
        self.assertEqual(expected, actual)
        
        actual = cache.get("key1")
        expected = "val1"
        self.assertEqual(expected, actual)
        
    def test_delete(self):
        cache = Memcache(namespace="unittest:")
        cache.put("key1", "val1")
        actual = cache.get("key1")
        expected = "val1"
        self.assertEqual(expected, actual)
        
        cache.delete("key1")
        actual = cache.get("key1")
        expected = None
        self.assertEqual(expected, actual)
        
        actual = self._memcache.get("unittest:key1")
        expected = "X"
        self.assertEqual(expected, actual)
        
    def test_non_string_storage(self):
        cache = Memcache(namespace="unittest:")
        cache.put("key1", {"hello": "world"})
        actual = cache.get("key1")
        expected = {"hello": "world"}
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    fixture.setup()
    unittest.main()