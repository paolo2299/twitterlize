from pyproj import Proj
from twitterlize.settings import Globe
from twitterlize import settings
import json
import os

class Geo(object):
    """Manipulate coordinates and resolve them to countries."""
    
    _countries = None
    _country_codes = None
    _lookup = None
    _resolution = Globe["grid"]["resolution_digits"]
    proj = Proj(proj=Globe["grid"]["projection"])

    @classmethod
    def countries(cls):
        if not cls._countries:
            cls._countries = cls._load_countries()
        return cls._countries

    @classmethod
    def country_codes(cls):
        return cls.countries().keys()

    @classmethod
    def get_country(cls, point):
        if not cls._lookup:
            cls._lookup = cls._load_lookup()
        try:
            proj_point = cls.proj(point[0], point[1], errcheck=True)
        except RuntimeError:
            return None
        proj_point = cls.snap_to_grid(proj_point)
        return cls._lookup.get(json.dumps(proj_point))

    @classmethod
    def snap_to_grid(cls, point):
        resolution = cls._resolution
        def _snap(coord):
            return int(round(coord, -1*resolution))
        return map(_snap, point)

    @staticmethod
    def reverse_coords(coords):
        return (coords[1], coords[0])

    @classmethod
    def _load_countries(cls):
        """Loads the list of countries from world-countries.json.
	    
	Returns a dictionary
            {country1: areas1,
             country2: areas2,
             ...
	    }

        Each country is a three-letter country code.
        Areas is a list of polygons defining the boundary of the country.
        Each polygon is a list of tuples (x,y).
        These polygon's are projected using the chosen projection.
	    
        """
        result = {}
        datapath = os.path.join(settings.DATA_FOLDER, "world-countries.json")
        data = json.loads(open(datapath).read())
        countries = data['features']
        for country in countries:
            code = country['id']
            areas = country['geometry']['coordinates']
            transareas = []
            for coords in areas:
                transcoords = []
                if len(coords[0]) > 2:
                    coords = coords[0]
                for point in coords:
                    tx, ty = cls.proj(point[0], point[1], errcheck=True)
                    transcoords.append((tx, ty))
                transareas.append(transcoords)
            result[code] = transareas
        return result

    @staticmethod
    def _load_lookup():
        datapath = os.path.join(settings.DATA_FOLDER, "country-lookup.json")
        return json.loads(open(datapath).read())

