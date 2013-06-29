import tweetstream
import time
import signal
from twitterlize.message.tweet import Tweet


class StreamingClient:
    def __init__(self, credentials, payload, store):
        self.count = 0
        self.last_reset = int(time.time())
        self.payload = payload
        self.stream = tweetstream.FilterStream
        self.twitterconf = credentials 
        self.store = store
        self.run_stream()

    def run_stream(self):
        print "starting stream"
        username = self.twitterconf['username']
        password = self.twitterconf['password']
        payload = self.payload
        print payload
        self.streaminst = self.stream(username, password, **payload)
        try:
            #set a timeout of 30 seconds with no tweets received
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(60)
            for tweet in self.streaminst:
                signal.alarm(60)
                ts = int(time.time())
                #every 10 minutes shut connection to allow reset
                #TODO(paul) needs to be more sophisticated - check for
                #when reset is actually needed
                if ts - self.last_reset >= 60*10:
                    self.last_reset = ts
                    self.close()
                    return True
                self.count += 1
                tw = Tweet(tweet)
                self.store.put(tw)
                if not self.count % 100:
                    print 'processed %s docs' % self.count
                
        except tweetstream.ConnectionError, e:
            print "Disconnected from twitter. Reason:", e.reason
            print "Reconnecting..."
            time.sleep(2)
            return False
    
    def timeout_handler(self, signum, frame):
        print "timeout signal received, restarting stream in 2 seconds..."
        time.sleep(2)
        print "raising exception"
        raise IOError()

    def close(self):
        if self.streaminst:
            self.streaminst.close()

