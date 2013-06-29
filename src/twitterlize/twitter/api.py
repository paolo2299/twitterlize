import tweepy
from twitterlize import settings

class TwitterAPI(tweepy.API):
    def __init__(self):
        consumer_key = settings.TwitterAPI["consumer_key"]
        consumer_secret = settings.TwitterAPI["consumer_secret"]
        token_key = settings.TwitterAPI["token_key"]
        token_secret = settings.TwitterAPI["token_secret"]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(token_key, token_secret)
	super(TwitterAPI, self).__init__(auth)

