import time
from twitterlize.datastore.mongo.store import MongoStore
from twitterlize.utils import get_timeslices


class CountStore(object):
    """Store counts of incoming items such as tweets, hashtags or user mentions.
    
    All counts are segmented by a segmentation (i.e. a country), entity_type 
    (i.e. "hashtag" or "user mention"), an entity and a time period.

    We segment the counts by time period so that a rolling tally over
    a restricted time period can be kept.

    """
    def __init__(self):
        self._store = MongoStore("CountStore")

    def put(self, entity_id, entity_type, segmentation, total_count=None):
        timeslices = get_timeslices()
        for timeslice in timeslices:
            match_criteria = {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "segmentation": segmentation,
                "timeslice": timeslice,
            }
            if total_count:
                #Note - This is non-atomic and so could cause inaccuracies
                #TODO: Implement locking
                existing = list(self._store.find(match_criteria))
                if existing:
                    existing = existing[0]
		    if existing.get("base_count"):
                        update_op = {
		            "$set": {
			        "count": total_count - existing["base_count"] + 1
			    }
	                }
		    else:
		        raise ValueError("Tried to increment doc with no base_count using total_count")
                else:
                    update_op = {
		        "$set": {
			    "base_count": total_count,
			    "count": 1
			}
	            }
            else:
                update_op = {
		    "$inc": {"count": 1}
		}
            self._store.update(match_criteria, update_op, upsert=True)

    def get_top(self, entity_type, segmentation, num_to_get, timestamp=None):
        """Get the top entities in this segmentation."""
        result = []
        timestamp = timestamp or int(time.time())
        #We use the latest COMPLETE timeslice, not the latest one
        timeslice = get_timeslices(timestamp)[-1]
        query = {
            "entity_type": entity_type,
            "segmentation": segmentation,
            "timeslice": timeslice,
        }
        fields = {
            "entity_id": 1,
            "count": 1,
        }
        docs = self._store.find(query, fields=fields).sort("count", -1).limit(num_to_get)
        for doc in docs:
            result.append((doc["entity_id"], doc["count"]))
        return result

