import unittest
from twitterlize.test.framework import fixture
from twitterlize import utils

class TestUtils(unittest.TestCase):
    
    def test_get_timeslices(self):
        jan_1st_2013_midday = fixture.jan_1st_2013_midday
        fifteen_mins = 60*15
        actual = utils.get_timeslices(jan_1st_2013_midday)
        expected = [
            jan_1st_2013_midday - fifteen_mins * 8,
            jan_1st_2013_midday - fifteen_mins * 7,
            jan_1st_2013_midday - fifteen_mins * 6,
            jan_1st_2013_midday - fifteen_mins * 5,
            jan_1st_2013_midday - fifteen_mins * 4,
            jan_1st_2013_midday - fifteen_mins * 3,
            jan_1st_2013_midday - fifteen_mins * 2,
            jan_1st_2013_midday - fifteen_mins * 1,
            jan_1st_2013_midday - fifteen_mins * 0, 
        ]
        self.assertEquals(expected, actual)
        
        actual = utils.get_timeslices(jan_1st_2013_midday + 1)
        expected = [
            jan_1st_2013_midday - fifteen_mins * 8,
            jan_1st_2013_midday - fifteen_mins * 7,
            jan_1st_2013_midday - fifteen_mins * 6,
            jan_1st_2013_midday - fifteen_mins * 5,
            jan_1st_2013_midday - fifteen_mins * 4,
            jan_1st_2013_midday - fifteen_mins * 3,
            jan_1st_2013_midday - fifteen_mins * 2,
            jan_1st_2013_midday - fifteen_mins * 1,
            jan_1st_2013_midday - fifteen_mins * 0, 
        ]
        self.assertEquals(expected, actual)
        
        actual = utils.get_timeslices(jan_1st_2013_midday - 1)
        expected = [
            jan_1st_2013_midday - fifteen_mins * 9,
            jan_1st_2013_midday - fifteen_mins * 8,
            jan_1st_2013_midday - fifteen_mins * 7,
            jan_1st_2013_midday - fifteen_mins * 6,
            jan_1st_2013_midday - fifteen_mins * 5,
            jan_1st_2013_midday - fifteen_mins * 4,
            jan_1st_2013_midday - fifteen_mins * 3,
            jan_1st_2013_midday - fifteen_mins * 2,
            jan_1st_2013_midday - fifteen_mins * 1, 
        ]
        self.assertEquals(expected, actual)

if __name__ == "__main__":
    fixture.setup()
    unittest.main()