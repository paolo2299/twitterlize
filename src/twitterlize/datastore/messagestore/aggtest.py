from pymongo import Connection
import json
import time

start = time.time()
conn = Connection()["Messages"]["tweetsample_mock"]
agg = conn.aggregate([
           {"$match":{"_id":{"$gte":"tw:1353160800", "$lt":"tw:1353160900"}}},
	   {"$project":{"hashtag":"$entities.hashtags"}},
	   {"$unwind":"$hashtag"},
	   {"$project":{"hashtag":"$hashtag.text"}},
	   {"$group":{
	       "_id": "$hashtag",
	       "count": {"$sum": 1}
	   }},
	   ]
      )
print len(agg['result'])
print str(time.time() - start)
