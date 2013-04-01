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

class MessageStore(MongoStore):
    """Mongodb datastore for holding messages.

    Examples of messages could include Twitter status updates, Facebook
    status updates, Youtube comments etc.

    """

    def __init__(self, storeid):
        super(MessageStore, self).__init__(storeid)
        self._config = settings.MongoStores[storeid]

    def put(self, message, entitytype="", segmentation="", entity="", timestamp=None):
        """Write a message to the store.
  
        Args:
	    message (twitterlize.message.Message) : Message object
	    entity (str) : Entity to use in the index.
	    timestamp (int) : Unix timestamp of message. 
	                      Defaults to using the 'timestamp'
			      method of the message class.

        """
        timestamp = timestamp or message.timestamp
        key = self.__class__.keyGen(entitytype, segmentation, entity, timestamp)
        doc = {"_id": key}
        doc.update(message.data)
        self.store.save(doc)

    @property
    def topentitystore(self):
        if not self._topentitystore:
            self._topentitystore = TopEntityStore(self._config["topentitystore"])
        return self._topentitystore

    def get_top(self, entitytype, segmentation, entity, timestamp=None, 
                                   fetch=settings.Aggregation["top_messages"]):
        to_timestamp = timestamp or time.time()
        from_timestamp = to_timestamp - settings.Aggregation["history"]
        key_from = self.__class__.keyGen(entitytype, segmentation, entity, from_timestamp)
        key_to = self.__class__.keyGen(entitytype, segmentation, entity, to_timestamp)
        messagecount = defaultdict(int)
        batch = 1
        while True:
            print "fetching batch %s" % batch
            found = False
            query = {'_id':{'$gt':key_from, '$lte':key_to}}
            docs = self.find(query).sort("_id", 1).limit(1000)
            for doc in docs:
                found = True
                key_from = doc["_id"]
                message = MessageAdapter.from_dict(entitytype, doc)
                id = message.id
                un = message.username
                sn = message.screen_name
                text = message.text
                messagecount[json.dumps((id,text,un,sn))] += 1
            batch += 1
            if not found:
                break
        return sorted(messagecount.items(), key=itemgetter(1), reverse=True)[:fetch]

    @staticmethod
    def keyGen(entitytype, segmentation, entity, timestamp):
        """Generate messagestore key for this message.

        Args:
	    segmentation (str): string representing a segmentation (up to five
	                        characters.
	                        e.g. a segmentation by country might look like
				     "CUSA".
	    entity (str): a string entity, such as a hashtag ("olympics"). Always
	                  padded (or cropped) so that it is forty characters.
	    timestamp (int): UNIX timestamp.

	    """
        rand = hexuuid(5)
        entitytype = pad2(entitytype)
        segmentation = pad5(segmentation)[:5]
        entity = pad(entity, 40)[:40]
        return ':'.join([entitytype, segmentation, entity, str(timestamp), rand])

