import time
from twitterlize.datastore.mongo.store import MongoStore
from twitterlize import settings
from twitterlize.utils import pad2, pad5, get_timeslice, add_dicts
from operator import itemgetter
from twitterlize.enums import EntityType

class TopEntityStore(MongoStore):
    """Store counts of entities extracted from messages.

    For example, counts of hastags and user_mentions occurring in tweets.
    We segment the counts by time period so that a rolling tally over
    a restricted time period can be kept.

    """
    def __init__(self):
        super(TopEntityStore, self).__init__("TopEntityStore")

    def put(self, message, timestamp=None):
        if not timestamp:
	    timestamp = message.timestamp
	    if not timestamp:
	        return
	timeslice = get_timeslice(timestamp)
	segs = message.segmentations
	entities = message.entities
	for segmentation in segs:
	    for entitytype, entities in message.entities.items():
	        for entity in entities:
	            key = self.__class__.keyGen(entitytype, segmentation, timeslice)
	            self.store.update({"_id":key},{"$inc":{entity: 1}}, upsert=True)

    def get_top(self, entitytype, segmentation, timestamp=None):
        """Get the top entities in this segmentation."""
	all_docs = []
	fetch = settings.Aggregation["top_entities"]
	timestamp = timestamp or int(time.time())
	segmentation = pad5(segmentation)
	to_timestamp = get_timeslice(timestamp)
	from_timestamp = to_timestamp - settings.Aggregation["history"]
        step = settings.Aggregation["timeslice_length"]
	current = from_timestamp
	while current <= to_timestamp:
            key = self.__class__.keyGen(entitytype, segmentation, current)
	    doc = self.find_one(key)
	    if doc:
	        del doc['_id']
	        all_docs.append(doc)
	    current += step
	result = add_dicts(all_docs)
	return sorted(result.items(), key=itemgetter(1), reverse=True)[:fetch]

    def get_top_multiple(self, entitytype, segs, timestamp=None):
        entitydicts = []
        for seg in segs:
	    entitydicts.append(dict(self.get_top(entitytype, seg, timestamp)))
	aggregated = add_dicts(entitydicts)
	return sorted(aggregated.items(), key=itemgetter(1), reverse=True)
	
    @staticmethod
    def keyGen(entitytype, segmentation, timeslice):
        entitytype = pad2(entitytype)
	segmentation = pad5(segmentation)
	return ':'.join([entitytype, segmentation, str(timeslice)])

