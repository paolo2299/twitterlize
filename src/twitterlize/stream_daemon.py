from twitterlize.web.twitter.streaming.client import StreamingClient
from twitterlize.datastore.topentitystore import TopEntityStore
from twitterlize.datastore.messagestore.tweetstore import TweetStore
from twitterlize.geo import Geo
from twitterlize.cache.redis import RedisCache
from twitterlize import settings
from twitterlize.enums import EntityType
from twitterlize.utils import utf8
import sys
from lockfile import FileLock
import time


def get_streaming_args(mode):
    payload = {}
    if mode == "locations":
        credentials = settings.Twitter['accounts'][0]
        payload['locations'] = ["-180,-90","180,90"]
        store = TopEntityStore()
    elif mode.startswith("entities"):
        idx = int(mode[-1])
        credentials = settings.Twitter['accounts'][idx]
        store = TweetStore()
        segs = ["C" + code for code in Geo.country_codes()]
        #We're only allowed to track 400 keywords
        lock = FileLock('/tmp/trackwords')
        with lock:
            all_hashtags = format_track(TopEntityStore().get_top_multiple(EntityType.TwitterHashtag, segs))
            all_usermentions = format_track(TopEntityStore().get_top_multiple(EntityType.TwitterUserMention, segs))
            used_hashtags, used_usermentions = get_used_trackwords(idx)
            used_hashtags, used_usermentions = set(used_hashtags), set(used_usermentions)
            hashtags = [ht for ht in all_hashtags if not ht in used_hashtags][:200]
            usermentions = [um for um in all_usermentions if not um in used_usermentions][:200]
            set_used_trackwords(idx, hashtags, usermentions)
            payload['track'] = hashtags + usermentions
    else:
        raise Exception("invalid mode: %s" % mode)
    return credentials, payload, store

def get_used_trackwords(not_this_index):
    used_hashtags, used_usermentions = [], []
    last_index = len(settings.Twitter["accounts"])
    indices = range(1, last_index)
    cache = RedisCache(namespace=settings.TrackwordCache["namespace"])
    for idx in indices:
        if idx == not_this_index:
            continue
        hashtag_key = "streamer%s:hashtags" % idx
        usermention_key = "streamer%s:usermentions" % idx
        hashtags = cache.get(hashtag_key) or []
        used_hashtags += hashtags
        usermentions = cache.get(usermention_key) or []
        used_usermentions += usermentions
    return used_hashtags, used_usermentions

def set_used_trackwords(idx, hashtags, usermentions):
    hashtag_key = "streamer%s:hashtags" % idx
    usermention_key = "streamer%s:usermentions" % idx
    cache = RedisCache(namespace=settings.TrackwordCache["namespace"])
    cache.put(hashtag_key, hashtags)
    cache.put(usermention_key, usermentions)
    
def reset_used_trackwords():
    last_index = len(settings.Twitter["accounts"])
    indices = range(1, last_index)
    for idx in indices:
        hashtag_key = "streamer%s:hashtags" % idx
        usermention_key = "streamer%s:usermentions" % idx
        cache = RedisCache(namespace=settings.TrackwordCache["namespace"])
        cache.delete(hashtag_key)
        cache.delete(usermention_key)

def format_track(words):
    return [utf8(w[0])[:60] for w in words]


if __name__ == "__main__":
    mode = sys.argv[1]
    retries = 0
    reset_used_trackwords()
    while True:
        credentials, payload, store = get_streaming_args(mode)
        while not mode == "locations" and not payload["track"]:
            credentials, payload, store = get_streaming_args(mode)
            if not payload["track"]:
                print "nothing to track. Trying again in 60 seconds"
                time.sleep(60)
        try:
            success = StreamingClient(credentials, payload, store)
        except IOError:
            success = False
        if not success:
            print "streaming failed, retrying..."
            retries += 1
            if retries > 20:
                raise Exception("Too many retries")
        else:
            #sufficient time has passed with no failures
            retries = 0

