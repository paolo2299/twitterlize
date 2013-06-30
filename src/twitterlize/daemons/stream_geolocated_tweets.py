from twitterlize.daemons.stream_daemon import StreamDaemon
from twitterlize.datastore.countstore import CountStore
from twitterlize import settings


class GeoTweetDaemon(StreamDaemon):
    
    def __init__(self):
        self._credentials = settings.Twitter['accounts'][0]
        self._payload = {'locations': ["-180,-90","180,90"]}
        self._countstore = CountStore()
    
    def _get_streaming_args(self):
        return self._credentials, self._payload
    
    def _payload_is_empty(self):
        return False
    
    def _on_tweet_callback(self, tweet):
        country_code = tweet.country_code
        if country_code:
            for entity_type, entities in tweet.entities.items():
                for entity_id in entities:
                    self._countstore.put(entity_id, entity_type, country_code)

if __name__ == "__main__":
    GeoTweetDaemon().stream()

