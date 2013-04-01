import time
import sys
from twitterlize.geo import Geo
from twitterlize.datastore.topentitystore import TopEntityStore
from twitterlize.datastore.messagestore.tweetstore import TweetStore
from twitterlize.cache.redis import RedisCache
from twitterlize import settings
from twitterlize.utils import serialize
from twitterlize.enums import EntityType
from twitterlize.web.twitter.api import TwitterAPI
import json

def cache_responses(t=None):
    #initialize stores
    ts = t or int(time.time())
    entitystore = TopEntityStore()
    tweetstore = TweetStore()
    entitytypes = [EntityType.TwitterHashtag, EntityType.TwitterUserMention]
    cache = RedisCache(namespace=settings.RequestCache["namespace"])
    html_cache = RedisCache(cachesecs=settings.HtmlCache["cachesecs"], 
                            namespace=settings.HtmlCache["namespace"])
    api = TwitterAPI()
    countries = Geo.country_codes()
    for country in countries:
        print country
        #debugging
        """
        if country == "USA":
        import pdb; pdb.set_trace()
        """
        response = {}
        segmentation = "C" + country
        for entitytype in entitytypes:
            response[entitytype] = []
            top_entities = entitystore.get_top(entitytype, segmentation, ts)[:8]
            for entity, count in top_entities:
                data = {"text":entity, "count":count, "tweets":[]}
                #TODO(paul) settings.EntityTypes.ALL = ""
                #TODO(paul) cache already retrieved entitytype/seg/entity combinations
                tweets = tweetstore.get_top(entitytype, "", entity, ts)[:5]
                for tweetdata, count in tweets:
                    data["tweets"].append({"html":tweet_html(tweetdata, html_cache, api), "count": count})
        response[entitytype].append(data)
        cache.put(segmentation, response)

def tweet_html(tweetdata, cache, api):
    html_template = cache.get("status_template")
    if not html_template:
        template_id = settings.HtmlCache["template_id"]
        html_template = api.get_oembed(template_id)["html"]
        cache.put("status_template", html_template)
    template_id = settings.HtmlCache["template_id"]
    template_text = settings.HtmlCache["template_text"]
    template_username = settings.HtmlCache["template_username"]
    template_screenname = settings.HtmlCache["template_screenname"]
    id, text, un, sn = json.loads(tweetdata)
    html_template = html_template.replace(template_id, str(id))
    html_template = html_template.replace(template_text, text)
    html_template = html_template.replace(template_username, un)
    html_template = html_template.replace(template_screenname, sn)
    return html_template

def run(interval):
    while True:
        cache_responses()
        time.sleep(interval)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'daemon':
        run(60)
    elif mode == 'cache':
        cache_responses()
    else:
        raise Exception('Invalid mode: %s' % mode)
