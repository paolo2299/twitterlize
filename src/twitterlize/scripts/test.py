from twitterlize.datastore.topentitystore import TopEntityStore
from twitterlize.datastore.messagestore.tweetstore import TweetStore

if __name__ == '__main__':
    f = open('/Users/paullawson/Data/twitter/tweets.json')
    store1 = TopEntityStore()
    store2 = TweetStore()
    x = store1.get_top("CGBR", timestamp=1356281700)
    y = store2.get_top("CGBR", x[0][0], timestamp=1356281700)
    import pdb; pdb.set_trace()
    pass
