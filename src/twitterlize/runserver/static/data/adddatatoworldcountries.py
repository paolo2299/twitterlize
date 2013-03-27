import json

g = json.loads(open('wikicountriesplusgeo').read())
d = json.loads(open('world-countries.json').read())

for f in d['features']:
    code = f['id']
    if code == "AFG":
        import pdb; pdb.set_trace()
    data = g.get(code)
    if data:
        url = data.get('url')
	location = data.get('location')
	code2 = data.get('code2')
	if url:
	    f['properties']['wiki'] = url
	if location:
	    f['properties']['geo'] = [location[1], location[0]]
	if code2:
	    f['properties']['code2'] = code2

d2 = open('wc2','w')
d2.write(json.dumps(d))
d2.close()
