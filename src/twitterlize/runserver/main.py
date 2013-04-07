#!/usr/bin/env python
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define
import tornado.web
from twitterlize.cache.redis import RedisCache
from twitterlize import settings

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
	    (r"/", MainHandler),
		]
        settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
			autoescape=None
			)
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        country = self.get_argument('code', 'USA')
        segmentation = "C" + country
        cache = RedisCache(namespace=settings.RequestCache["namespace"])
        data = cache.get(segmentation)
        self.render(
		    "index.html",
                    page_title = "Twitterlyze | Home",
		    intro = "Most talked about in the last hour...",
		    footer_text = "For more information, please email us at <a href=\"mailto:twitterlize@gmail.com\">twitterlize@gmail.com</a>.",
                    hashtags = extract_entities(data, "ht"),
                    users = extract_entities(data, "um"),
		    hashtag_tweets = extract_tweets(data, "ht"),
		    user_tweets = extract_tweets(data, "um"),
		  )

def getpercent(numer, denom):
    return int(float(numer)*100/denom)

def extract_entities(data, entitytype, num=10):
    result = []
    entities = data[entitytype][:num]
    if entities:
        maxcount = entities[0]["count"]
        for e in entities:
            result.append({"text":e["text"],
	                   "count":e["count"],
		           "percent":getpercent(e["count"], maxcount)
            })
    return result

def extract_tweets(data, entitytype, numentities=10, numtweets=20):
    result = []
    entities = data[entitytype][:numentities]
    for e in entities:
        result.append((e["text"], e["tweets"][:numtweets]))
    return result
        

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
