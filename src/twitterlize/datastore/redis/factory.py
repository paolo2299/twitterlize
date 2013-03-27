from redis import StrictRedis
from twitterlize import settings

class RedisFactory(object):

    _redis = None

    @classmethod
    def getconn(cls):
        """Return cached connection if it exists.
	Otherwise, create a new connection and cache it.

	"""
	if not cls._redis:
            redisconf = settings.Redis
	    cls._redis = StrictRedis(redisconf["host"], redisconf["port"])
	return cls._redis

