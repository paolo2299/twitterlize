import time
from twitterlize import settings
from twitterlize.cache import CacheType

jan_1st_2013_midday = 1357041600

def setup():
    setup_aggregation_settings()
    setup_database_settings()
    setup_mock_time()
    
def setup_aggregation_settings():
    settings.Aggregation = {
        "timeslice_granularity": 60*15,  #15 minutes
        "history": 3600*2,
        "top_entities": 3,
        "top_tweets": 3,
    }
    
def setup_database_settings():
    settings.MongoStores["TweetStore"]["dbname"] = "twitterlize_unittest"
    settings.MongoStores["TweetStore"]["cache_namespace"] = "tws_unittest"
    
    settings.MongoStores["CountStore"]["dbname"] = "twitterlize_unittest"
    settings.MongoStores["CountStore"]["cache_namespace"] = "cts_unittest"
    
    settings.MongoStores["unittest"] = {
        "host": settings.EnvSettings.mongohost,
        "port": settings.EnvSettings.mongoport,
        "dbname": "twitterlize_unittest",
        "collection": "unittest",
        "cachetype": CacheType.Off,
    }
    
def setup_mock_time():
    def mock_time():
        return jan_1st_2013_midday
    time.time = mock_time