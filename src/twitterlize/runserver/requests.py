class Endpoint(object):
    """Data and metadata for an endpoint."""
    def __init__(self, confid):
        try:
            self._conf = settings.Endpoints[confid]
	except KeyError:
	    raise Exception("Unknown endpoint ID: %s" % confid)

    @property
    def url(self):
        return self._conf["url"]

    @property
    def cachekey(self):
        return self._conf.get("cachekey")
    
