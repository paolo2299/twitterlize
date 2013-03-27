import uuid
import hashlib
from twitterlize import settings
import json

def add_dicts(ds):
    def add_two_dicts(d1,d2):
        return dict((n, d1.get(n, 0)+d2.get(n, 0)) for n in set(d1).union(d2) )
    accumulator = {}
    if ds:
        ds = iter(ds)
        accumulator = ds.next()
        for d in ds:
            accumulator = add_two_dicts(accumulator, d)
    return accumulator

def hexuuid(digits=32):
    """Generate a hexidecimal random string.
    
    Args:
        digits (int): number of digits. Max 32. Min 1. Default 32.

    """
    return str(uuid.uuid4())[(-1)*digits:]

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

def get_timeslice(timestamp):
    interval = int(settings.Aggregation["timeslice_length"])
    return (timestamp/interval)*interval

def hexhash(data, digits=32):
    """Generate a hexidecimal hash of data.
    
    Args:
        data (str): data you want to hash.
        digits (int): number of digits. Max 32. Min 1. Default 32.

    """
    m = hashlib.md5()
    m.update(data)
    h = m.hexdigest()
    return h[(-1)*digits:]

#TODO - more approriate serilaizations method? If it's already a string just leave as a string?
#TODO - does memcache require utf8-encoded strings?
def serialize(data):
    return json.dumps(data)

def deserialize(data):
    return json.loads(data)
    
def pad(text, numchars):
    return text.ljust(numchars,'-')

def pad2(text):
    return pad(text, 2)

def pad3(text):
    return pad(text, 3)

def pad4(text):
    return pad(text, 4)

def pad5(text):
    return pad(text, 5)

def pad6(text):
    return pad(text, 6)

def pad7(text):
    return pad(text, 7)

def pad8(text):
    return pad(text, 8)

def pad9(text):
    return pad(text, 9)

def pad10(text):
    return pad(text, 10)
