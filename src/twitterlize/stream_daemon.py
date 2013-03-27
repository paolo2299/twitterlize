from twitterlize.web.twitter.streaming.client import StreamingClient
from twitterlize.datastore.topentitystore import TopEntityStore
from twitterlize.datastore.messagestore.tweetstore import TweetStore
from twitterlize.geo import Geo
from twitterlize import settings
from twitterlize.enums import EntityType
from twitterlize.utils import utf8
import sys

def get_streaming_args(mode):
    payload = {}
    if mode == "locations":
        credentials = settings.Twitter['accounts'][0]
        payload['locations'] = ["-180,-90","180,90"]
	store = TopEntityStore()
    elif mode in ["entities1", "entities2", "entities3"]:
        idx = int(mode[-1])
        credentials = settings.Twitter['accounts'][idx]
	store = TweetStore()
        segs = ["C" + code for code in Geo.country_codes()]
        all_hashtags = TopEntityStore().get_top_multiple(EntityType.TwitterHashtag, segs)
        all_usermentions = TopEntityStore().get_top_multiple(EntityType.TwitterUserMention, segs)
        #We're only allowed to track 400 keywords
	hashtags = [format_track(ht[0]) for ht in all_hashtags[(idx-1)*200: idx*200]]
	usermentions = [format_track(um[0]) for um in all_usermentions[(idx-1)*200: idx*200]]
	payload['track'] = hashtags + usermentions
	#payload['track'] = ['foursquare']
    else:
        raise Exception("invalid mode: %s" % mode)
    return credentials, payload, store

def format_track(x):
    #TODO(paul) does this correctly crop to 60 bytes?
    return utf8(x)[:60]

if __name__ == "__main__":
    mode = sys.argv[1]
    retries = 0
    while True:
        credentials, payload, store = get_streaming_args(mode)
        try:
            success = StreamingClient(credentials, payload, store)
        except IOError:
            success = False
        if not success:
            print "streaming failed, retrying..."
            retries+=1
            if retries>20:
                raise Exception("Too many retries")

