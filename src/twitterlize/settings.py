from twitterlize.cache import CacheType
import os

class EnvSettings():
    """Environment-specific settings."""
    mongohost = "localhost"
    mongoport = 27017
    redishost = "localhost"
    redisport = 6379
    memcachedhost = "localhost"
    memcachedport = 11211
    homedir = os.path.expanduser("~")
    repository = os.path.join(os.path.expanduser("~"), "projects", "twitterlize2", "src")

DATA_FOLDER = os.path.join(EnvSettings.repository, "twitterlize", "data")

Aggregation = {
               "timeslice_length": 60*5,
	       "history": 3600*3,
	       "top_entities": 20,
	       "top_messages": 20,
              }

Globe = {
         "grid":{
	         "projection": "goode",
		     "resolution_digits": 4
		}
	}

RequestCache = {
                "namespace": "rqc:"
               }

TrackwordCache = {
                "namespace": "twc:"
                }

TESTMODE = False
TEST_SUFFIX = TESTMODE and "_test" or ""

Twitter = {
           "accounts": 
	       [
	         {
		  "username": "paolo_lawson",
                  "password": "*******"
		 },
                 {
		  "username": "PaoloLawson",
                  "password": "*******"
		 },
	       ],
	   }

TwitterAPI = {
              "consumer_key": "FWYye62J1KXIlRRBgNczAg",
              "consumer_secret": "********",
              "token_key": "367131116-bk4e1YwP9WNG5m6UQq1NFseChZbjDOFm6JmPAmrl",
              "token_secret": "********"
             }

HtmlCache = {
             "cachesecs": 3600,
	     "namespace": "htmlcache:",
	     "template_id": "214321492496887808",
	     "template_text": "hello all feet",
	     "template_username": "Paul Lawson",
	     "template_screenname": "paolo_lawson"
            }

Redis = {
         "host": EnvSettings.redishost,
	 "port": EnvSettings.redisport,
	 "namespace": TEST_SUFFIX
        }

Memcache = {
            "host": EnvSettings.memcachedhost,
	    "port": EnvSettings.memcachedport,
	    "namespace": TEST_SUFFIX
           }

MessageStoresDB = "Messages" + TEST_SUFFIX
MessageEntitiesDB = "MessageEntities" + TEST_SUFFIX
PersonDB = "Person" + TEST_SUFFIX

MessageTypes = {
                "tweet":{
		    "abbreviation":"tw",
		},
	       }
                

MongoStores = {
                 #### MessageStores ###
                 "TweetStore":{
		           "host": EnvSettings.mongohost,
                           "port": EnvSettings.mongoport,
			   "dbname": MessageStoresDB,
			   "collection": "tweets",
			   "cachetype": CacheType.Off,
			   "abbreviation": "tw",
                          },
                 #### TopEntityStores ###
                 "TopEntityStore":{
		           "host": EnvSettings.mongohost,
                           "port": EnvSettings.mongoport,
			   "dbname": MessageEntitiesDB,
			   "collection": "counts",
			   "cachetype": CacheType.Off,
			   "abbreviation": "te",
                          },
                 ### Person Stores ###
                 "PersonData":{
		           "host": EnvSettings.mongohost,
                           "port": EnvSettings.mongoport,
			   "dbname": PersonDB,
			   "collection": "networkdata",
			   "cachetype": CacheType.Volatile,
			   "abbreviation": "pd",
                          },
                 "DataSourceToPersonID":{
		           "host": EnvSettings.mongohost,
                           "port": EnvSettings.mongoport,
			   "dbname": PersonDB,
			   "collection": "datasourcetopersonid",
			   "cachetype": CacheType.Volatile,
			   "abbreviation": "dstp",
                          },
              }
