from twitterlize.datastore.countstore import CountStore
from twitterlize.datastore.tweetstore import TweetStore
from twitterlize.geo import Geo
from twitterlize.cache.redis import RedisCache
from twitterlize import settings
from twitterlize.utils import utf8
import sys
from lockfile import FileLock

class KeywordsTweetDaemon(object):
    
    def __init__(self, daemon_number):
        super(KeywordsTweetDaemon, self).__init__()
        if daemon_number == 0:
            raise ValueError("daemon_number must be 1 or higher")
        self._daemon_number = daemon_number
        self._countstore = CountStore()
        self._tweetstore = TweetStore()
    
    def _get_streaming_args(self):
        self._credentials = settings.Twitter['accounts'][self._daemon_number]
        segs = ["C" + code for code in Geo.country_codes()]
        #We're only allowed to track 400 keywords
        lock = FileLock('/tmp/trackwords')
        with lock:
            all_hashtags = self._get_all_entities("hashtag", segs)
            all_usermentions = self._get_all_entities("user_mention", segs)
            used_hashtags, used_usermentions = map(set, self._get_used_trackwords())
            hashtags = [ht for ht in all_hashtags if not ht in used_hashtags][:200]
            usermentions = [um for um in all_usermentions if not um in used_usermentions][:200]
            self._set_used_trackwords(hashtags, usermentions)
            self._payload = {'track': hashtags + usermentions}
        return self._credentials, self._payload
    
    def _on_tweet_callback(self, tweet):
        self._tweetstore.put(tweet)
        tweet_id = tweet.original_id
        for entity_type, entities in tweet.entities.items():
            for entity in entities:
                segmentation = ":".join([entity_type, entity])
                self._countstore.put(tweet_id, "tweet", segmentation)
    
    def _get_all_entities(self, entity_type, segmentations):
        fetch = settings.Aggregation["top_entities"]
        get_top_entities_for_seg = lambda s: set(self._countstore.get_top( 
                                                        entity_type=entity_type, 
                                                        segmentation=s, 
                                                        num_to_get=fetch).keys())
        top_entities = map(get_top_entities_for_seg, segmentations)
        return list(reduce(lambda x, y : x | y, top_entities))
         
    def _payload_is_empty(self):
        return not self._payload or not self._payload['track']

    def _get_used_trackwords(self):
        used_hashtags, used_usermentions = [], []
        last_index = len(settings.Twitter["accounts"])
        indices = range(1, last_index)
        cache = RedisCache(namespace=settings.TrackwordCache["namespace"])
        for idx in indices:
            if idx == self._daemon_number:
                continue
            hashtag_key = "streamer%s:hashtags" % idx
            usermention_key = "streamer%s:usermentions" % idx
            hashtags = cache.get(hashtag_key) or []
            used_hashtags += hashtags
            usermentions = cache.get(usermention_key) or []
            used_usermentions += usermentions
        return used_hashtags, used_usermentions
    
    def _set_used_trackwords(self, hashtags, usermentions):
        hashtag_key = "streamer%s:hashtags" % self._daemon_number
        usermention_key = "streamer%s:usermentions" % self._daemon_number
        cache = RedisCache(namespace=settings.TrackwordCache["namespace"])
        cache.put(hashtag_key, hashtags)
        cache.put(usermention_key, usermentions)
        
    def _reset_used_trackwords(self):
        last_index = len(settings.Twitter["accounts"])
        indices = range(1, last_index)
        for idx in indices:
            hashtag_key = "streamer%s:hashtags" % idx
            usermention_key = "streamer%s:usermentions" % idx
            cache = RedisCache(namespace=settings.TrackwordCache["namespace"])
            cache.delete(hashtag_key)
            cache.delete(usermention_key)            

    def _filter_track(self, words):
        return [utf8(w[0]) for w in words if utf8(w[0])[:60] == utf8(w[0])]


if __name__ == "__main__":
    daemon_number = int(sys.argv[1])
    KeywordsTweetDaemon(daemon_number).stream()

