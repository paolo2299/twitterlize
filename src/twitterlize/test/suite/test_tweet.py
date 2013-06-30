from twitterlize.test.framework import example_tweet
from twitterlize.test.framework import fixture
import unittest
from twitterlize.tweet import Tweet

class TestTweet(unittest.TestCase):
    
    def setUp(self):
        self.tweet = Tweet(example_tweet.tweet)
        self.retweet = Tweet(example_tweet.retweet)
        self.retweet_from_db = Tweet(example_tweet.retweet_from_database)
    
    def test_id(self):
        self.assertEqual(318687071210446848, self.tweet.id)
        self.assertEqual(318687071223021569, self.retweet.id)
        self.assertEqual(318685578843521025, self.retweet_from_db.id)
        
    def test_original_id(self):
        self.assertEqual(318687071210446848, self.tweet.original_id)
        self.assertEqual(318685578843521025, self.retweet.original_id)
        self.assertEqual(318685578843521025, self.retweet_from_db.original_id)
        
    def test_text(self):
        tweeted_text = "(NWS) kak :D RT @liadinatasarii: Ini kenapa nama pd disingkat semua -__- @fadhilahpermata (FPS) @MeilizaFahrilia (SMF) @febriilia (FAS)"
        retweeted_text = "1) If you're Justin Bieber RT this.   2) Follow everybody who RTed it.   3) Follow me I follow back.   #JustinFollowAllJustins"
        self.assertEqual(tweeted_text, self.tweet.text)
        self.assertEqual(retweeted_text, self.retweet.text)
        self.assertEqual(retweeted_text, self.retweet_from_db.text)
        
    def test_author(self):
        self.assertEqual(42594318, self.tweet.author)
        self.assertEqual(1036906466, self.retweet.author)
        self.assertEqual(1036906466, self.retweet_from_db.author)
        
    def test_authorpic(self):
        tweet_authorpic = "http://a0.twimg.com/profile_images/3458401841/8d6fc05fc3d07add7ec3d10fdd98ad90_normal.jpeg"
        retweeted_authorpic = "http://a0.twimg.com/profile_images/3460972249/6eefba2da18157ac7807448394cc796f_normal.jpeg"
        self.assertEqual(tweet_authorpic, self.tweet.authorpic)
        self.assertEqual(retweeted_authorpic, self.retweet.authorpic)
        self.assertEqual(retweeted_authorpic, self.retweet_from_db.authorpic)
        
    def test_username(self):
        self.assertEqual("F.P.S", self.tweet.username)
        self.assertEqual("Justin Bieber", self.retweet.username)
        self.assertEqual("Justin Bieber", self.retweet_from_db.username)
        
    def test_screenname(self):
        self.assertEqual("fadhilahpermata", self.tweet.screen_name)
        self.assertEqual("TrueBieberB0y", self.retweet.screen_name)
        self.assertEqual("TrueBieberB0y", self.retweet_from_db.screen_name)
        
    def test_entities(self):
        tweet_entities = {
            "hashtag": [
            ],
            "user_mention": [
                "liadinatasarii",
                "fadhilahpermata",
                "MeilizaFahrilia",
                "febriilia",
            ],
        }
        retweet_entities = {
            "hashtag": [
                "JustinFollowAllJustins",
            ],
            "user_mention": [
            ],
        }
        self.assertEqual(tweet_entities, self.tweet.entities)
        self.assertEqual(retweet_entities, self.retweet.entities)
        self.assertEqual(retweet_entities, self.retweet_from_db.entities)
    
    def test_country_code(self):
        self.assertEqual("CDEU", self.tweet.country_code)
        #retweets never contain geo information
        self.assertEqual(None, self.retweet.country_code)
        self.assertEqual(None, self.retweet_from_db.country_code)
        
    def test_timestamp(self):
        self.assertEqual(1364812293, self.tweet.timestamp)
        self.assertEqual(1364812293, self.retweet.timestamp)
        self.assertEqual(1364811937, self.retweet_from_db.timestamp)
        
    def test_original_timestamp(self):
        self.assertEqual(1364812293, self.tweet.original_timestamp)
        self.assertEqual(1364811937, self.retweet.original_timestamp)
        self.assertEqual(1364811937, self.retweet_from_db.original_timestamp)
        
    def test_is_retweet(self):
        self.assertEqual(False, self.tweet.is_retweet)
        self.assertEqual(True, self.retweet.is_retweet)
        self.assertEqual(True, self.retweet_from_db.is_retweet)

if __name__ == "__main__":
    fixture.setup()
    unittest.main()
