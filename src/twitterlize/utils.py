import time
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

def get_timeslices(timestamp=None):
    timestamp = timestamp or int(time.time())
    timeslices = []
    granularity = int(settings.Aggregation["timeslice_granularity"])
    history = int(settings.Aggregation["history"])
    timeslice = ((timestamp - history)/granularity)*granularity
    while timeslice <= timestamp:
        timeslices.append(timeslice)
        timeslice += granularity
    return timeslices

def serialize(data):
    if isinstance(data, basestring):
        return data
    return json.dumps(data)

def deserialize(data):
    try:
        return json.loads(data)
    except ValueError:
        return data
    