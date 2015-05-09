"""
.. module:: bidr.apps.auctions.test_forms
   :synopsis: Bidr Silent Auction System Auction Form Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.test.testcases import TestCase

from .forms import AuctionCreateForm


class TestAuctionCreateForm(TestCase):

    def test_form_valid_all_fields(self):
        data = {"name": "test_name", "description": "test", "start_time": "2015-05-09 03:12", "end_time": "2015-06-03 03:12", "bid_increment": "2.00", "optional_password": "test"}
        form = AuctionCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_times(self):
        data = {"name": "test_name", "description": "test", "end_time": "2015-05-09 03:12", "start_time": "2015-06-03 03:12", "bid_increment": "2.00", "optional_password": "test"}
        form = AuctionCreateForm(data=data)
        self.assertFalse(form.is_valid())
