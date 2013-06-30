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
            update_op = {}
            if total_count:
                #Note - This is non-atomic and so could cause inaccuracies
                #TODO: Implement locking
                existing = self._store.find(match_criteria)
                if existing:
                    existing = list(existing)[0]
                    increment = total_count - existing["min_count"]
                else:
                    update_op["$set"] = {"min_count": total_count}
                    increment = 1
            else:
                update_op["$set"] = {"min_count": 0}
                increment = 1
            update_op["$inc"] = increment
            self._store.update(match_criteria, update_op, upsert=True)

    def get_top(self, entity_type, segmentation, num_to_get, timestamp=None):
        """Get the top entities in this segmentation."""
        result = []
        timestamp = timestamp or int(time.time())
        #We use the latest COMPLETE timeslice, not the latest one
        timeslice = get_timeslices(timestamp)[-2]
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

