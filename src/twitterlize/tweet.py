from email.utils import parsedate
import time
from twitterlize.geo import Geo


class Tweet():
    """Twitter status update."""

    DEFAULT_SEGS = [
		    ""  #make sure all tweets are recorded  
		   ]

    def __init__(self, data):
        self.data = data

    @property
    def id(self):
        """See superclass docstring."""
        self.data.get("id")
    
    @property
    def original_id(self):
        """See superclass docstring."""
        return self.original_data.get("id")

    @property
    def text(self):
        """See superclass docstring."""
        return self.original_data.get("text")

    @property
    def author(self):
        """See superclass docstring."""
        return str(self.original_data.get("user", {}).get("id"))

    @property
    def authorpic(self):
        """See superclass docstring."""
        return self.original_data.get("user", {}).get("profile_image_url")

    @property
    def username(self):
        """See superclass docstring."""
        return self.original_data.get("user", {}).get("name")

    @property
    def screen_name(self):
        """See superclass docstring."""
        return self.original_data.get("user", {}).get("screen_name")

    @property
    def entities(self):
        entities = self.original_data.get('entities', {})
        hashtags = [h["text"] for h in entities.get('hashtags', [])]
        usermentions = [um["screen_name"] for um in entities.get('user_mentions', [])]
        return {"hashtag": hashtags, 
                "user_mention": usermentions}

    @property
    def country_code(self):
        geotags = self.original_data.get("coordinates")
        if geotags:
            coords = geotags.get("coordinates")
            if coords:
                country = Geo.get_country(coords)
                if country: 
                    return "C" + country
        return None

    @property
    def timestamp(self):
        if not self.data.get("created_at"):
            return None
        return int(time.mktime(parsedate(self.data["created_at"])))
    
    @property
    def original_timestamp(self):
        if not self.original_data.get("created_at"):
            return None
        return int(time.mktime(parsedate(self.original_data["created_at"]))) 

    @property
    def is_retweet(self):
        return "retweeted_status" in self.data or "data_from_retweet" in self.data
    
    @property
    def original_data(self):
        if self.is_retweet:
            return self.retweet_data
        return self.data

    @property
    def retweet_data(self):
        if "data_from_retweet" in self.data:
            return self.data
        return self.data.get("retweeted_status", {})

