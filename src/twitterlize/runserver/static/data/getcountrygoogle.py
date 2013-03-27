import requests
import json

d = json.loads(open("wikicountries.json").read())

import pdb; pdb.set_trace()
for code, data in d.items():
    code2 = data["code2"]
    if code2 == "AF":
        pdb.set_trace()
    url = "http://maps.google.com/maps/api/geocode/json?components=country:%s&sensor=false" % code2
    resp = requests.get(url)
    if resp.content:
        try: 
	    res = json.loads(resp.content)
	except:
	    pass
	if type(res) == dict and res.get('results'):
            res0 = res['results'][0]
	    location = res0.get('geometry',{}).get('location',{})
	    if location and res0['address_components'][0]['short_name'] == code2:
                lat = location['lat']
                lng = location['lng']
                d[code]['location'] = [lat, lng]

f = open('wikicountriesplusgeo', 'w')
f.write(json.dumps(d))
