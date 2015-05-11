"""
.. module:: bidr.apps.core.templatetags.test_currency
   :synopsis: Bidr Silent Auction System Core Template Tag and Filter Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from decimal import Decimal

from django.test.testcases import TestCase

from .templatetags.currency import currency


class TestCurrency(TestCase):

    def test_none(self):
        self.assertEqual("$0.00", currency(None))

    def test_int(self):
        self.assertEqual("$5.00", currency(5))

    def test_str(self):
        self.assertEqual("$7.76", currency("7.76"))

    def test_float(self):
        self.assertEqual("$8.19", currency(8.19))

    def test_positive(self):
        self.assertEqual("$3.23", currency(Decimal("3.23")))

    def test_negative(self):
        self.assertEqual("-$3.23", currency(Decimal("-3.23")))
