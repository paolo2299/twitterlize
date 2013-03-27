from pyproj import Proj
import os
import json
from twitterlize import settings
import time
from twitterlize.geo import Geo

def point_in_poly(x,y,poly):
    """Usage:
    poly = [(0,0),(0,2),(1,1),(2,2),(2,0)]

    print point_in_poly(1,0.5, poly) //True
    print point_in_poly(1.75,1.5, poly) //True
    print point_in_poly(1,1.5, poly) //False

    """
    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def min_max_coords(countries):
    min_x, max_x, min_y, max_y = None, None, None, None
    for areas in countries.values():
        for coords in areas:
	    for x,y in coords:
	        min_x = min_x and min(x, min_x) or x
	        max_x = max_x and max(x, max_x) or x
	        min_y = min_y and min(y, min_y) or y
	        max_y = max_y and max(y, max_y) or y
    return min_x, min_y, max_x, max_y

def locate(point, countries, boundaries, projected=False):
    result = []
    x, y = point[0], point[1]
    if not projected:
        projection = settings.Globe["grid"]["projection"]
        proj = Proj(proj=projection)
        try:
            point = proj(point[0], point[1], errcheck=True)
            x, y = round_to_grid(point[0]), round_to_grid(point[1])
        except:
            return result

    for country, areas in countries.items():
        minx, miny, maxx, maxy = boundaries[country]
        if x < minx or x > maxx or y < miny or y > maxy:
	    continue
        for coords in areas:
            if point_in_poly(x, y, coords):
	        result.append(country)
		break
    located = None
    if result:
        if len(result) > 1:
	    if result[0] == "LSO" or result[1] == "LSO":
	        located = "LSO"
	    elif result[0] == "FRA" or result[1] == "FRA":
	        located = "FRA"
	else:
	    if result:
	        located = result[0]
    return located

def round_to_grid(x):
    digits = settings.Globe["grid"]["resolution_digits"]
    return int(round(x, -1*digits))

def get_country_boundaries(countries):
    boundaries = {}
    for country, areas in countries.items():
        minx, maxx, miny, maxy = None, None, None, None
	for area in areas:
	    for coord in area:
	        c_x, c_y = coord[0], coord[1]
	        minx = minx and min(c_x, minx) or c_x
	        miny = miny and min(c_y, miny) or c_y
	        maxx = maxx and max(c_x, maxx) or c_x
	        maxy = maxy and max(c_y, maxy) or c_y
	boundaries[country] = (minx, miny, maxx, maxy)
    return boundaries

def generate_lookup(countries):
    start = time.time()
    print "populating grid"
    lookup = {}
    min_x, min_y, max_x, max_y = min_max_coords(countries)
    #round to grid resolution
    projection = settings.Globe["grid"]["projection"]
    proj = Proj(proj=projection)
    digits = settings.Globe["grid"]["resolution_digits"]
    min_x = round_to_grid(min_x)
    max_x = round_to_grid(max_x)
    min_y = round_to_grid(min_y)
    max_y = round_to_grid(max_y)
    step = 10**(digits)
    steps_x = (max_x - min_x)/step
    steps_y = (max_y - min_y)/step
    total_points = (steps_x + 1)*(steps_y + 1)
    c = 0
    added = 0
    boundaries = get_country_boundaries(countries)
    for i_x in range(steps_x + 1):
        for i_y in range(steps_y + 1):
	    point = (min_x + i_x*step, min_y + i_y*step)
	    #Check if point belongs to projection
	    try:
	        proj(point[0], point[1], inverse=True, errcheck=True)
		#check point is in a country
		found = locate(point, countries, boundaries, projected=True)
                if found:
                    lookup[json.dumps(point)] = found
		    added += 1
	    except RuntimeError:
	        pass
	    c += 1
	    if not c % 10000:
	        print "processed %s of %s (%s added) in %s" % (c, total_points, added, round(time.time() - start, 1))
    return lookup

if __name__ == "__main__":
    countries = Geo.countries()
    lookup = generate_lookup(countries)
    datapath = os.path.join(settings.DATAFOLDER, "country-lookup.json")
    g = open(datapath, 'w')
    g.write(json.dumps(lookup))
    g.close()

