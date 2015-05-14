"""
.. module:: bidr.apps.auctions.test_utils
   :synopsis: Bidr Silent Auction System Auction Utilities Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test.testcases import TestCase

from ..auctions.models import Auction, STAGES
from ..bids.models import Bid
from ..items.models import Item
from .utils import _end_auction


class TestEndAuction(TestCase):

    def setUp(self):  # noqa
        self.auction_instance = Auction.objects.create(name="test",
                                                       description="test",
                                                       start_time=datetime.now(),
                                                       end_time=datetime.now() + timedelta(days=20))

        # Unbid items shouldn't affect the outcome.
        unbid_item = Item.objects.create(name="unbid_item", starting_bid=10)
        self.auction_instance.bidables.add(unbid_item)

        user = get_user_model().objects.create_user("The Dude", "thedudeabides@dudeism.com", "+13107824229", "!")

        # Create an item with bids that has yet to be claimed.
        self.bid_item1 = Item.objects.create(name="Bowling Ball", starting_bid=10)
        self.bid1 = Bid.objects.create(user=user, amount=22)
        self.bid_item1.bids.add(self.bid1)

        # Create another item with bids that has yet to be claimed.
        self.bid_item2 = Item.objects.create(name="Rug", starting_bid=500)
        self.bid2 = Bid.objects.create(user=user, amount=2200)
        self.bid_item2.bids.add(self.bid2)

        self.auction_instance.bidables.add(self.bid_item1)
        self.auction_instance.bidables.add(self.bid_item2)

    def test_with_unclaimed_items(self):
        """If unclaimed items exist in an auction, the stage gets set to claim."""

        new_stage = _end_auction(self.auction_instance)

        self.assertEqual(STAGES.index("Claim"), new_stage)

    def test_with_claimed_items(self):
        """If all items in an auction are claimed, the stage gets set to report."""

        self.bid_item1.claim(self.bid1)
        self.bid_item2.claim(self.bid2)

        new_stage = _end_auction(self.auction_instance)
        self.assertEqual(STAGES.index("Report"), new_stage)

    def test_with_mixed_items(self):
        """In the case of both claimed and unclaimed items, the stage gets set to claim, where unclaimed items don't appear."""

        self.bid_item2.claim(self.bid2)

        new_stage = _end_auction(self.auction_instance)
        self.assertEqual(STAGES.index("Claim"), new_stage)

    def test_auction_already_ended_claim(self):
        self.test_with_unclaimed_items()

        old_stage = self.auction_instance.stage

        # Should still be claim
        new_stage = _end_auction(self.auction_instance)
        self.assertEqual(old_stage, new_stage, "The stage changed.")
        self.assertEqual(STAGES.index("Claim"), new_stage)

    def test_auction_already_ended_report(self):
        self.test_with_claimed_items()

        old_stage = self.auction_instance.stage

        # Should still be report
        new_stage = _end_auction(self.auction_instance)
        self.assertEqual(old_stage, new_stage, "The stage changed.")
        self.assertEqual(STAGES.index("Report"), new_stage)
