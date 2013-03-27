class CacheType(object):
    """Enumeration of available cache types."""
    Off = 0
    Volatile = 1
    Persistent = 2

class Cache(object):
    """Cache interface."""
    def put(self, key, data):
        raise NotImplementedError()

    def get(self, key):
        raise NotImplementedError()

    def delete(self, key):
        raise NotImplementedError()

    def expire(self, key, seconds):
        raise NotImplementedError()

