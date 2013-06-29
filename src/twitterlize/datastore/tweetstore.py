from twitterlize.datastore.mongo.store import MongoStore
from twitterlize.tweet import Tweet


class TweetStore(object):
    """Mongodb datastore for holding tweets.

    """

    def __init__(self):
        self._store = MongoStore("TweetStore")

    def put(self, tweet, timestamp=None):
        """Write a tweet to the store.
  
        Args:
	    tweet (twitterlize.tweet.Tweet) : Tweet object

        """
        doc = {"_id": tweet.original_data["id"]}
        doc.update(tweet.original_data)
        if tweet.is_retweet:
            doc["data_from_retweet"] = True
        self._store.save(doc)

    def get(self, tweet_id):
        doc = self._store.find_one(tweet_id)
        if doc:
            return Tweet(doc)
        return None
    