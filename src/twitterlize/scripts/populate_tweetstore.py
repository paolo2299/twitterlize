from twitterlize.datastore.messagestore.tweetstore import TweetStore
from twitterlize.datastore.topentitystore import TopEntityStore
from twitterlize.message.tweet import Tweet
from twitterlize import settings
from email.utils import parsedate
import json
import os
import time

def run(datapath):
    tweetstore = TweetStore()
    topentitystore = TopEntityStore()
    with open(datapath) as f:
        c = 0
        for line in f:
	    rawtweet = json.loads(line)
	    if rawtweet.get("created_at"):
	        tweet = Tweet(rawtweet)
	        tweetstore.put(tweet)
	        topentitystore.put(tweet)
	    c += 1
	    if not c % 1000:
	        print "tweets stored: %s" % c

if __name__ == "__main__":
    datapath = os.path.join(settings.EnvSettings.homedir, 
                                  "Data", "twitter", "tweets.json")
    run(datapath)
