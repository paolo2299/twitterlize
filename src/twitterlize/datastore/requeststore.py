from twitterlize.cache.redis import RedisCache


class RequestCache(object):
    """Store request responses in Redis for fast access.
    These are generated at regular intervals by daemons.

    """
    
    KEYS = {}

    _cache = None

    @class
    def getStore()
