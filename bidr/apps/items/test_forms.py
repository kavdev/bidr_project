"""
.. module:: bidr.apps.items.test_forms
   :synopsis: Bidr Silent Auction System Item Form Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from decimal import Decimal

from django.test.testcases import TestCase

from .forms import ItemCreateForm


class TestItemCreateForm(TestCase):

    def test_form_valid(self):
        data = {"name": "test_item", "description": "test_item_description", "starting_bid": Decimal("1.00")}
        form = ItemCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_int_price(self):
        data = {"name": "test_item", "description": "test_item_description", "starting_bid": 5}
        form = ItemCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_name(self):
        data = {"description": "test_item_description", "starting_bid": Decimal("1.00")}
        form = ItemCreateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("name", form.errors)
