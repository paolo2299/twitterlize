import time
from twitterlize import settings
from twitterlize.cache import CacheType
from twitterlize.test.framework.redis import Redis

jan_1st_2013_midday = 1357041600

def setup():
    setup_aggregation_settings()
    setup_database_settings()
    setup_mock_time()
    clear_redis_unittest()
    
def setup_aggregation_settings():
    settings.Aggregation = {
        "timeslice_granularity": 60*15,  #15 minutes
        "history": 3600*2,
        "top_entities": 3,
        "top_tweets": 3,
    }
    
def setup_database_settings():
    settings.MongoStores["TweetStore"]["dbname"] = "twitterlize_unittest"
    settings.MongoStores["TweetStore"]["cachetype"] = CacheType.Off
    settings.MongoStores["TweetStore"]["cache_namespace"] = "unittest_tws"
    
    settings.MongoStores["CountStore"]["dbname"] = "twitterlize_unittest"
    settings.MongoStores["CountStore"]["cachetype"] = CacheType.Off
    settings.MongoStores["CountStore"]["cache_namespace"] = "unittest_cts"
    
    settings.MongoStores["unittest"] = {
        "host": settings.EnvSettings.mongohost,
        "port": settings.EnvSettings.mongoport,
        "dbname": "twitterlize_unittest",
        "collection": "unittest",
        "cachetype": CacheType.Off,
        "cache_namespace": "unittest:"
    }
    
def setup_mock_time():
    def mock_time():
        return jan_1st_2013_midday
    time.time = mock_time
    
def clear_redis_unittest():
    Redis().clear()
    
