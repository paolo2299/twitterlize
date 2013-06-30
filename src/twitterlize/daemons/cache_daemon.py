import time
import sys
from twitterlize.geo import Geo
from twitterlize.datastore.countstore import CountStore
from twitterlize.datastore.tweetstore import TweetStore
from twitterlize.cache.rediscache import RedisCache
from twitterlize import settings


def cache_top_tweets():
    #initialize stores
    ts = int(time.time())
    countstore = CountStore()
    tweetstore = TweetStore()
    cache = RedisCache(namespace=settings.TopTweetsCache["namespace"])
    countries = Geo.country_codes()
    top_tweets_cache = {}
    for country in countries:
        print "*************"
        print country
        print "*************"
        
        top_tweets = {}
        segmentation = "C" + country
        for entitytype in ["hashtag", "user_mention"]:
            top_tweets[entitytype] = []
            top_entities = countstore.get_top(entitytype, 
                                              segmentation,
                                              settings.Aggregation['top_entities'],
                                              ts)
            for entity, count in top_entities:
                data = {"text":entity, "count":count, "tweets":[]}
                tweets = top_tweets_cache.get((entitytype, entity, ts))
                if not tweets:
                    print "fetching tweets for " + str((entitytype, entity, ts))
                    segmentation = ":".join([entitytype, entity])
                    tweets = countstore.get_top("tweet", 
                                                segmentation,
                                                settings.Aggregation['top_tweets'], 
                                                ts)
                    tweets = map(lambda x: (tweetstore.get(x[0]), x[1]), tweets)
                    top_tweets_cache[(entitytype, entity, ts)] = tweets
                for tweet, count in tweets:
                    data["tweets"].append({"tweet":tweet.data, "count": count})
                top_tweets[entitytype].append(data)
        cache.put(segmentation, top_tweets)

def run(interval):
    while True:
        cache_top_tweets()
        time.sleep(interval)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'daemon':
        run(60)
    elif mode == 'cache':
        cache_top_tweets()
    else:
        raise Exception('Invalid mode: %s' % mode)
