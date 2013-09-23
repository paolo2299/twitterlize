from twitterlize.test.framework import fixture
from twitterlize.test.framework.mongo import Mongo
from twitterlize.utils import serialize
import unittest
from twitterlize import settings
from twitterlize.datastore.countstore import CountStore
from copy import copy


class CountStoreTest(unittest.TestCase):
    
    def setUp(self):
        fixture.setup_database_settings()
        fixture.setup_mock_time()
        self._mongo = Mongo("CountStore")
        self._mongo.clear()

    def build_timeslice_docs(self, doc):
        timeslices = [
            fixture.jan_1st_2013_midday - 8*60*15,
            fixture.jan_1st_2013_midday - 7*60*15,
            fixture.jan_1st_2013_midday - 6*60*15,
            fixture.jan_1st_2013_midday - 5*60*15,
            fixture.jan_1st_2013_midday - 4*60*15,
            fixture.jan_1st_2013_midday - 3*60*15,
            fixture.jan_1st_2013_midday - 2*60*15,
            fixture.jan_1st_2013_midday - 60*15,
            fixture.jan_1st_2013_midday,
        ]

    def build_doc(orig_doc, timeslice):
        doc = copy(orig_doc)
        doc["timeslice"] = timeslice
        return doc
	return map(lambda ts: build_doc(doc, ts), timeslices)

    def delete_ids(self, docs):
        for doc in docs:
            del doc['_id']

    def get_all_docs(self):
        docs = list(self._mongo.find().sort('timeslice', 1))
        self.delete_ids(docs)
        return docs

    def test_put_no_total_count(self):
        countstore = CountStore()
        countstore.put("entity1", "test_entity", "test_seg")
        docs = self.get_all_docs()

        self.assertEqual(9, len(docs))

        expected = self.build_timeslice_docs({
            "entity_id"   : "entity1",
            "entity_type" : "test_entity",
            "segmentation": "test_seg",
            "count"       : 1,
        })
        self.assertEqual(expected, docs)

        fixture.setup_mock_time(fixture.jan_1st_2013_midday + 60*15)

        countstore.put("entity1", "test_entity", "test_seg")
        docs = self.get_all_docs()

        self.assertEqual(10, len(docs))

        expected = self.build_timeslice_docs({
            "entity_id"   : "entity1",
            "entity_type" : "test_entity",
            "segmentation": "test_seg",
            "count"       : 2,
        })

        expected[0]["count"] = 1
        last_doc = copy(expected[-1])
        last_doc["count"] = 1
        last_doc["timeslice"] = fixture.jan_1st_2013_midday + 60*15
        expected.append(last_doc)

        self.assertEqual(expected, docs)

    def test_put_with_total_count(self):
        countstore = CountStore()
        countstore.put("entity1", "test_entity", "test_seg", total_count = 10)
        docs = self.get_all_docs()

        self.assertEqual(9, len(docs))

        expected = self.build_timeslice_docs({
            "entity_id"   : "entity1",
            "entity_type" : "test_entity",
            "segmentation": "test_seg",
            "base_count"  : 10,
            "count"       : 1,
        })
        self.assertEqual(expected, docs)

        fixture.setup_mock_time(fixture.jan_1st_2013_midday + 60*15)

        countstore.put("entity1", "test_entity", "test_seg", total_count = 15)
        docs = self.get_all_docs()

        self.assertEqual(10, len(docs))

        expected = self.build_timeslice_docs({
            "entity_id"   : "entity1",
            "entity_type" : "test_entity",
            "segmentation": "test_seg",
            "count"       : 6,
	        "base_count"  : 10,
        })
        expected[0]["count"] = 1
        expected[0]["base_count"] = 10
        last_doc = copy(expected[-1])
        last_doc["count"] = 1
        last_doc["base_count"] = 15
        last_doc["timeslice"] = fixture.jan_1st_2013_midday + 60*15
        expected.append(last_doc)

        self.assertEqual(expected, docs)

    def test_get_top(self):
        countstore = CountStore()
        countstore.put("entity1", "test_entity", "test_seg")
        countstore.put("entity2", "test_entity", "test_seg")
        countstore.put("entity2", "test_entity", "test_seg")
        actual = countstore.get_top("test_entity", "test_seg", 10)
        expected = [("entity2", 2), ("entity1", 1)]

        self.assertEqual(expected, actual)

        fixture.setup_mock_time(fixture.jan_1st_2013_midday + 3600)

        countstore.put("entity1", "test_entity", "test_seg")
        countstore.put("entity1", "test_entity", "test_seg")
        countstore.put("entity3", "test_entity", "test_seg")
        actual = countstore.get_top("test_entity", "test_seg", 10)
        expected = [("entity1", 3), ("entity2", 2), ("entity3", 1)]

        self.assertEqual(expected, actual)

        fixture.setup_mock_time(fixture.jan_1st_2013_midday + 2*3600)

        countstore.put("entity3", "test_entity", "test_seg")
        countstore.put("entity3", "test_entity", "test_seg")
        actual = countstore.get_top("test_entity", "test_seg", 10)
        expected = [("entity3", 3), ("entity1", 2)]

        self.assertEqual(expected, actual)

    
if __name__ == "__main__":
    fixture.setup()
    unittest.main()
