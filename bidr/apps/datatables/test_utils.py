"""
.. module:: bidr.apps.datatables.test_utils
   :synopsis: Bidr Silent Auction System Datatable Utility Tests

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.test.testcases import TestCase
from .utils import dict_merge


class TestDictMerge(TestCase):

    def test_base_non_dict(self):
        self.assertEqual(None, dict_merge(None, {"hello": "world"}))

    def test_merge_non_dict(self):
        self.assertEqual("sam", dict_merge({"hello": "world"}, "sam"))

    def test_one_level_dict_merge(self):
        self.assertEqual({"hello": "world", "goodbye": "world"},
                         dict_merge({"hello": "world"}, {"goodbye": "world"}))

    def test_one_level_dict_overwrite(self):
        self.assertEqual({"hello": {"world", "sun"}},
                         dict_merge({"hello": "world"}, {"hello": {"world", "sun"}}))

    def test_two_level_dict_merge(self):
        self.assertEqual(
            {"hello": {"world": "today", "toy": "boat"}, "goodbye": "world"},
            dict_merge({"hello": {"world": "today"}}, {"goodbye": "world", "hello": {"toy": "boat"}})
        )

    def test_two_level_dict_overwrite(self):
        self.assertEqual(
            {"hello": {"world": "tomorrow"}, "goodbye": "world"},
            dict_merge({"hello": {"world": "today"}}, {"goodbye": "world", "hello": {"world": "tomorrow"}})
        )
