from twitterlize.message import Message
from email.utils import parsedate
import time
from twitterlize.geo import Geo
from twitterlize.enums import EntityType


class Tweet(Message):
    """Twitter status update."""

    TYPEID = "tweet"
    DEFAULT_SEGS = [
		    ""  #make sure all tweets are recorded  
		   ]

    def _parse(self, message):
        """See superclass docstring."""
        return message

    @property
    def text(self):
        """See superclass docstring."""
	if self.is_retweet:
	    return self.retweet_data.get("text")
        return self.data.get("text")

    @property
    def author(self):
        """See superclass docstring."""
	if self.is_retweet:
	    return str(self.retweet_data.get("user", {}).get("id"))
        return str(self.data.get("user", {}).get("id"))

    @property
    def authorpic(self):
        """See superclass docstring."""
	if self.is_retweet:
	    return self.retweet_data.get("user", {}).get("profile_image_url")
        return self.data.get("user", {}).get("profile_image_url")

    @property
    def entities(self):
        data = self.data
	if self.is_retweet:
	    data = self.retweet_data
        entities = data.get('entities', {})
        hashtags = [h["text"] for h in entities.get('hashtags', [])]
	usermentions = [um["screen_name"] for um in entities.get('user_mentions', [])]
	return {EntityType.TwitterHashtag: hashtags, 
	        EntityType.TwitterUserMention: usermentions}

    @property
    def segmentations(self):
        segs = self.__class__.DEFAULT_SEGS[:]
        data = self.data
	if self.is_retweet:
	    data = self.retweet_data
	geotags = data.get("coordinates")
	if geotags:
	    coords = geotags.get("coordinates")
	    if coords:
	        country = Geo.get_country(coords)
	        if country: 
	            segmentation = "C" + country
		    segs.append(segmentation)
	return segs

    @property
    def timestamp(self):
        if not self.data.get("created_at"):
	    return None
        return int(time.mktime(parsedate(self.data["created_at"]))) 

    @property
    def is_retweet(self):
        return "retweeted_status" in self.data

    @property
    def retweet_data(self):
        return self.data.get("retweeted_status", {})

