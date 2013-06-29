from twitterlize.twitter.streaming.client import StreamingClient
import time


class StreamDaemon(object):
    
    def __init__(self):
        self._payload = None
        self._credentials = None
        self._callback = None
    
    def get_streaming_args(self):
        raise NotImplementedError()
    
    def payload_is_empty(self):
        raise NotImplementedError()
    
    def _on_tweet_callback(self):
        raise NotImplementedError()
    
    def stream(self):
        retries = 0
        while True:
            credentials, payload = self.get_streaming_args()
            while self.payload_is_empty:
                print "nothing to track. Trying again in 60 seconds"
                time.sleep(60)
                credentials, payload = self.get_streaming_args()
            try:
                success = StreamingClient(credentials, payload, self._on_tweet_callback)
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
