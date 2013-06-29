from pymongo import Connection
from twitterlize import settings
from twitterlize.cache import CacheType
from twitterlize.datastore.mongo.store import MongoStore
from twitterlize.datastore.topentitystore import TopEntityStore
from twitterlize.message.adapter import MessageAdapter
from twitterlize.utils import hexuuid, pad2, pad3, pad5, pad
from collections import defaultdict
from operator import itemgetter
import time
import json
from bson.objectid import ObjectId

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
        if not timestamp:
            timestamp = tweet.timestamp
            if not timestamp:
                return
        for segmentation in tweet.segmentations:
            for entitytype, entities in tweet.entities.items():
                for entity in entities:
                    meta = {
                        "segmentation": segmentation,
                        "entity_type": entitytype,
                        "entity": entity,
                        "timestamp": timestamp,
                    }
        doc = {"meta": meta, "tweet": tweet.data}
        self._store.save(doc)

    def get_top(self, segmentation, entitytype, entity, timestamp=None, 
                                   fetch=settings.Aggregation["top_messages"]):
        to_timestamp = timestamp or time.time()
        from_timestamp = to_timestamp - settings.Aggregation["history"]
        query = {
            "meta.segmentation": segmentation,
            "meta.entity_type": entitytype,
            "meta.entity": entity,
            "meta.timestamp": {"$gte": from_timestamp, "$lte": to_timestamp},
        }
        messagecount = defaultdict(int)
        key_from = ObjectId("0"*24)
        batch = 1
        while True:
            print "fetching batch %s" % batch
            found = False
            query["_id"] = {"$gt": key_from}
            docs = self.find(query).sort("_id", 1).limit(1000)
            for doc in docs:
                found = True
                key_from = doc["_id"]
                tweet = Tweet.from_dict(doc["tweet"])
                messagecount[tweet] += 1
            batch += 1
            if not found:
                break
        return sorted(messagecount.items(), key=itemgetter(1), reverse=True)[:fetch]

