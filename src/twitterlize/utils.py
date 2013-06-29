import uuid
import hashlib
from twitterlize import settings
import json

def utf8(x):
    if isinstance(x, unicode):
        return x.encode('utf8')
    elif isinstance(x, str):
        # Check encoded sensibly in UTF-8
        x.decode('utf8')
        return x
    raise Exception("value %s must be utf8-encoded string or unicode" % x)

def url_encode_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        out_dict[utf8(k)] = utf8(v)
    return out_dict 

def get_timeslices(timestamp):
    timeslices = []
    granularity = int(settings.Aggregation["timeslice_granularity"])
    history = int(settings.Aggregation["history"])
    timeslice = ((timestamp - history)/granularity)*granularity
    while timeslice < timestamp:
        timeslices.append(timeslice)
        timeslice += granularity
    return timeslices

def serialize(data):
    return json.dumps(data)

def deserialize(data):
    return json.loads(data)
    