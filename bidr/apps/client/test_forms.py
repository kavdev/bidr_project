"""
.. module:: bidr.apps.client.test_forms
   :synopsis: Bidr Silent Auction System Form Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from datetime import datetime, timedelta

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

    def test_form_valid_no_password(self):
        data = {"auction_id": self.auction_instance.id}
        form = AddAuctionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_no_password_password_provided(self):
        """
        Submitting a password for an auction that doesn't need one should be fine.
        The form just ignores it.
        """

        data = {"auction_id": self.auction_instance.id}
        form = AddAuctionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_no_password(self):
        """A bogus auction ID will fail this test."""

        data = {"auction_id": 2012311243}
        form = AddAuctionForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_valid_with_password(self):
        self.auction_instance.optional_password = "test"
        self.auction_instance.save()

        data = {"auction_id": self.auction_instance.id, "optional_password": "test"}
        form = AddAuctionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_password_incorrect_password_provided(self):
        self.auction_instance.optional_password = "test"
        self.auction_instance.save()

        data = {"auction_id": self.auction_instance.id, "optional_password": "not_test"}
        form = AddAuctionForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_with_password_no_password_provided(self):
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
                                                       bid_increment=2)

        self.item_instance = Item.objects.create(name="Bowling Ball", starting_bid=10)
        self.auction_instance.bidables.add(self.item_instance)

    def test_form_valid(self):
        data = {"amount": 13}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        data = {"amount": 13.121234}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())

    def test_valid_bid_matches(self):
        data = {"amount": 12}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_bid_below_starting_bid(self):
        data = {"amount": 2}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_second_bid_below_highest_bid(self):
        user = get_user_model().objects.create_user("The Dude", "thedudeabides@dudeism.com", "+13107824229", "!")

        # Create an item with bids that has yet to be claimed.
        self.bid1 = Bid.objects.create(user=user, amount=22)
        self.item_instance.bids.add(self.bid1)

        data = {"amount": 21}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_second_bid_above_highest_bid_below_increment(self):
        user = get_user_model().objects.create_user("The Dude", "thedudeabides@dudeism.com", "+13107824229", "!")

        # Create an item with bids that has yet to be claimed.
        self.bid1 = Bid.objects.create(user=user, amount=22)
        self.item_instance.bids.add(self.bid1)

        data = {"amount": 23}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())

    def test_form_valid_second_bid_above_highest_bid_below_matches_increment(self):
        user = get_user_model().objects.create_user("The Dude", "thedudeabides@dudeism.com", "+13107824229", "!")

        # Create an item with bids that has yet to be claimed.
        self.bid1 = Bid.objects.create(user=user, amount=22)
        self.item_instance.bids.add(self.bid1)

        data = {"amount": 24}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_auction_already_ended_stage(self):
        self.auction_instance.stage = STAGES.index("Report")
        self.auction_instance.save()

        data = {"amount": 24}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_auction_already_ended_time(self):
        self.auction_instance.end_time = datetime.now() - timedelta(minutes=5)
        self.auction_instance.save()

        data = {"amount": 24}
        form = AddBidForm(item_instance=self.item_instance, auction_instance=self.auction_instance, data=data)
        self.assertFalse(form.is_valid())
