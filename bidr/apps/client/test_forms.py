"""
.. module:: bidr.apps.client.test_forms
   :synopsis: Bidr Silent Auction System Form Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test.testcases import TestCase

from ..bids.models import Bid
from ..auctions.models import Auction, STAGES
from ..items.models import Item
from .forms import AddAuctionForm, AddBidForm


class TestAddAuctionForm(TestCase):

    def setUp(self):  # noqa
        self.auction_instance = Auction.objects.create(name="test",
                                                       description="test",
                                                       start_time=datetime.now(),
                                                       end_time=datetime.now() + timedelta(days=20))

    def test_valid_form_no_password(self):
        data = {"auction_id": self.auction_instance.id}
        form = AddAuctionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_form_no_password_password_provided(self):
        """
        Submitting a password for an auction that doesn't need one should be fine.
        The form just ignores it.
        """

        data = {"auction_id": self.auction_instance.id}
        form = AddAuctionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_no_password(self):
        """A bogus auction ID will fail this test."""

        data = {"auction_id": 2012311243}
        form = AddAuctionForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_form_with_password(self):
        self.auction_instance.optional_password = "test"
        self.auction_instance.save()

        data = {"auction_id": self.auction_instance.id, "optional_password": "test"}
        form = AddAuctionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_with_password_incorrect_password_provided(self):
        self.auction_instance.optional_password = "test"
        self.auction_instance.save()

        data = {"auction_id": self.auction_instance.id, "optional_password": "not_test"}
        form = AddAuctionForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_with_password_no_password_provided(self):
        self.auction_instance.optional_password = "test"
        self.auction_instance.save()

        data = {"auction_id": self.auction_instance.id}
        form = AddAuctionForm(data=data)
        self.assertFalse(form.is_valid())


class TestAddBidForm(TestCase):

    def setUp(self):  # noqa
        self.auction_instance = Auction.objects.create(name="test",
                                                       description="test",
                                                       start_time=datetime.now(),
                                                       end_time=datetime.now() + timedelta(days=20),
                                                       bid_increment=Decimal("2.00"))

        self.item_instance = Item.objects.create(name="Bowling Ball", minimum_price=Decimal("10.00"))
        self.auction_instance.bidables.add(self.item_instance)

    def test_valid_form(self):
        data = {"amount": Decimal("13.00")}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_bid_matches(self):
        data = {"amount": Decimal("12.00")}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_bid_below_minimum_price(self):
        data = {"amount": Decimal("2.00")}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_second_bid_below_highest_bid(self):
        user = get_user_model().objects.create_user("The Dude", "thedudeabides@dudeism.com", "+13107824229", "!")

        # Create an item with bids that has yet to be claimed.
        self.bid1 = Bid.objects.create(user=user, amount=Decimal("22.00"))
        self.item_instance.bids.add(self.bid1)

        data = {"amount": Decimal("21.00")}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_second_bid_above_highest_bid_below_increment(self):
        user = get_user_model().objects.create_user("The Dude", "thedudeabides@dudeism.com", "+13107824229", "!")

        # Create an item with bids that has yet to be claimed.
        self.bid1 = Bid.objects.create(user=user, amount=Decimal("22.00"))
        self.item_instance.bids.add(self.bid1)

        data = {"amount": Decimal("23.00")}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_auction_already_ended_stage(self):
        self.auction_instance.stage = STAGES.index("Report")
        self.auction_instance.save()

        data = {"amount": Decimal("24.00")}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_auction_already_ended_time(self):
        self.auction_instance.end_time = datetime.now() - timedelta(minutes=5)
        self.auction_instance.save()

        data = {"amount": Decimal("24.00")}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())
