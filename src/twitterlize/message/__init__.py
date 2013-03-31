from twitterlize.utils import hexhash
from twitterlize.enums import EntityType


class Message(object):
    """Baseclass to represent a message and associated metadata.

    A message can be something like a tweet, or a Facebook status update,
    or a Youtube comment etc.

    This class should always be subclassed, not used directly.

    """
    def __init__(self, data, raw=True):
        """Construct a message object.

	Args:
	    data (mixed): object containing message and message metadata.
	                  If raw==True, this will be parsed using the subclass' 
			  parse method.
			  If raw==False, this should be a dict of the form
			  returned by the _parse method.

	"""
        if raw:
            self.data = self._parse(data)
        else:
            self.data = data

    def _parse(self, data):
        """Parse the data used to construct this object.

        Args:
	    data (mixed): object containing message and message metadata.
	Returns:
	    (dict): dict of message data, suitable for storing in mongoDB.

        """
        raise NotImplementedError("Subclass %s of Message needs to \
                                            implement _parse method" % self.__class__)

    def _utf8(self, text):
        """Convert text from the native storage format to utf8.
	This default implementation assumes text is unicode. The method should be
	overridden in the subclass if this is not the case.

        Args:
	    text (str): text that needs converting.
	Returns:
	    (str): text encoded as a utf8 string.

        """
        if type(text) != unicode:
            raise Exception("Non-unicode text passed to Message._utf8: %s" % text)
        return text.encode('utf8')

    @property
    def id(self):
        """Get message native ID.

    Returns:
        (str): message native ID.

    """
        raise NotImplementedError("Subclass %s of Message needs to \
                                            implement id method" % self.__class__)

    @property
    def text(self):
        """Get message text.

	Returns:
	    (str): message text.

	"""
        raise NotImplementedError("Subclass %s of Message needs to \
                                            implement text method" % self.__class__)

    @property
    def author(self):
        """Generate hex uuid of author.

	Returns:
	    (str): unique ID of message author.

	"""
        raise NotImplementedError("Subclass %s of Message needs to \
                                            implement author method" % self.__class__)

    @property
    def authoruuid(self):
        """Generate hex uuid of message author. Ensures uniqueness across different 
	           message types.

	    Returns:
	        (str): hex uuid of message author. 

	    """
        return hexhash(':'.join([self.__class__.TYPEID, self.author]))

    @property
    def authorpic(self):
        """Get url of author's picture.

	    Returns:
	        (str): url of author's picture.

	    """
        raise NotImplementedError("Subclass %s of Message needs to \
                                            implement picture method" % self.__class__)
    @property
    def timestamp(self):
        """Get timestamp of message.

	    Returns:
	        (int): UNIX timestamp of message.

	    """
        raise NotImplementedError("Subclass %s of Message needs to \
                                            implement timestamp method" % self.__class__)
