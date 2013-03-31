from twitterlize.datastore.messagestore import MessageStore


class TweetStore(MessageStore):
    def __init__(self):
        super(TweetStore, self).__init__("TweetStore")

    def put(self, tweet, timestamp=None):
        """Write a message to all tweet stores, and increment
	any entities in the relevant TopEntityStores.
  
        Args:
	    message (twitterlize.message.Message) : Message object
	    timestamp (int) : Unix timestamp of message. 
	                      Defaults to using the 'timestamp'
			      method of the message class.

        """
        if not timestamp:
            timestamp = tweet.timestamp
            if not timestamp:
                return
        segs = tweet.segmentations
        for segmentation in segs:
            for entitytype, entities in tweet.entities.items():
                for entity in entities:
                    super(TweetStore, self).put(tweet, entitytype, segmentation, entity, timestamp)

