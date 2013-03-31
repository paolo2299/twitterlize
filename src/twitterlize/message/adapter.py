from twitterlize.enums import EntityType
from twitterlize.message.tweet import Tweet

class MessageAdapter(object):
    
    @staticmethod
    def from_dict(entitytype, data):
        #Only tweets exist so far
        if entitytype in [
                    EntityType.TwitterHashtag,
                    EntityType.TwitterUserMention
                ]:
            return Tweet(data)
        