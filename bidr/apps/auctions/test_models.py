"""
.. module:: bidr.apps.auctions.test_models
   :synopsis: Bidr Silent Auction System Auction Model Tests.

.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>
.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now

from ..bids.models import Bid
from ..items.models import Item
from .models import Auction


class AuctionTest(TestCase):

    def setUp(self):
        # Generate users
        self.user1 = get_user_model().objects.create_user(
            email="testuser1@bidrapp.com",
            name="testuser1",
            phone_number="+13105550001",
            password="password"
        )
        self.user2 = get_user_model().objects.create_user(
            email="testuser2@bidrapp.com",
            name="testuser2",
            phone_number="+13105550002",
            password="password"
        )
        self.user3 = get_user_model().objects.create_user(
            email="testuser3@bidrapp.com",
            name="testuser3",
            phone_number="+13105550003",
            password="password"
        )
        self.user4 = get_user_model().objects.create_user(
            email="testuser4@bidrapp.com",
            name="testuser4",
            phone_number="+13105550004",
            password="password"
        )

        # Generate Bids
        self.bid1 = Bid.objects.create(amount=1, user=self.user1)
        self.bid2 = Bid.objects.create(amount=2, user=self.user1)
        self.bid3 = Bid.objects.create(amount=3, user=self.user1)
        self.bid4 = Bid.objects.create(amount=4, user=self.user1)
        self.bid5 = Bid.objects.create(amount=1, user=self.user2)
        self.bid6 = Bid.objects.create(amount=2, user=self.user2)
        self.bid7 = Bid.objects.create(amount=3, user=self.user2)
        self.bid8 = Bid.objects.create(amount=4, user=self.user2)
        self.bid9 = Bid.objects.create(amount=1, user=self.user3)
        self.bid10 = Bid.objects.create(amount=2, user=self.user3)
        self.bid11 = Bid.objects.create(amount=3, user=self.user3)
        self.bid12 = Bid.objects.create(amount=4, user=self.user3)
        self.bid13 = Bid.objects.create(amount=1, user=self.user4)
        self.bid14 = Bid.objects.create(amount=2, user=self.user4)
        self.bid15 = Bid.objects.create(amount=3, user=self.user4)
        self.bid16 = Bid.objects.create(amount=4, user=self.user4)
        self.bid17 = Bid.objects.create(amount=5, user=self.user4)
        self.bid18 = Bid.objects.create(amount=6, user=self.user3)

        # Generate Items
        self.item1 = Item.objects.create(name="item1", description="test item 1")
        self.item2 = Item.objects.create(name="item2", description="test item 2")
        self.item3 = Item.objects.create(name="item3", description="test item 3")
        self.item4 = Item.objects.create(name="item4", description="test item 4")
        self.item5 = Item.objects.create(name="item5", description="test item 5")
        self.item6 = Item.objects.create(name="item6", description="test item 6")
        self.item7 = Item.objects.create(name="item7", description="test item 7")
        self.item8 = Item.objects.create(name="item8", description="test item 8")
        self.item9 = Item.objects.create(name="item9", description="test item 9")
        self.item10 = Item.objects.create(name="item10", description="test item 10")
        self.item11 = Item.objects.create(name="item11", description="test item 11")
        self.item12 = Item.objects.create(name="item12", description="test item 12")
        self.item13 = Item.objects.create(name="item13", description="test item 13")
        self.item14 = Item.objects.create(name="item14", description="test item 14")
        self.item15 = Item.objects.create(name="item15", description="test item 15")

        # Generate End date-time fields
        auciton_end_time = now() + timedelta(days=5)

        # Generate Auction
        self.auction1 = Auction.objects.create(
            name="test1",
            description="test auction 1.",
            stage=0,
            end_time=auciton_end_time
        )
        self.auction2 = Auction.objects.create(
            name="test2",
            description="test auction 2.",
            stage=1,
            end_time=auciton_end_time
        )
        self.auction3 = Auction.objects.create(
            name="test3",
            description="test auction 3.",
            stage=2,
            end_time=auciton_end_time
        )
        self.auction4 = Auction.objects.create(
            name="test4",
            description="test auction 4.",
            stage=3,
            end_time=auciton_end_time
        )

        # Set up stuff
        self.auction1.bidables.add(self.item1)
        self.auction1.bidables.add(self.item2)
        self.auction1.bidables.add(self.item3)
        self.auction2.bidables.add(self.item4)
        self.auction2.bidables.add(self.item5)
        self.auction2.bidables.add(self.item6)
        self.auction3.bidables.add(self.item7)
        self.auction3.bidables.add(self.item8)
        self.auction3.bidables.add(self.item9)
        self.auction4.bidables.add(self.item10)
        self.auction4.bidables.add(self.item11)
        self.auction4.bidables.add(self.item12)
        self.auction2.bidables.add(self.item13)
        self.auction3.bidables.add(self.item14)
        self.auction4.bidables.add(self.item15)
        self.auction1.participants.add(self.user1)
        self.auction1.participants.add(self.user2)
        self.auction1.participants.add(self.user3)
        self.auction1.participants.add(self.user4)
        self.auction2.participants.add(self.user1)
        self.auction2.participants.add(self.user2)
        self.auction2.participants.add(self.user3)
        self.auction2.participants.add(self.user4)
        self.auction3.participants.add(self.user1)
        self.auction3.participants.add(self.user2)
        self.auction3.participants.add(self.user3)
        self.auction3.participants.add(self.user4)
        self.auction4.participants.add(self.user1)
        self.auction4.participants.add(self.user2)
        self.auction4.participants.add(self.user3)
        self.auction4.participants.add(self.user4)
        self.item4.bids.add(self.bid1)
        self.item4.bids.add(self.bid6)
        self.item5.bids.add(self.bid2)
        self.item5.bids.add(self.bid7)
        self.item6.bids.add(self.bid3)
        self.item6.bids.add(self.bid8)
        self.item7.bids.add(self.bid4)
        self.item7.bids.add(self.bid5)
        self.item8.bids.add(self.bid9)
        self.item8.bids.add(self.bid14)
        self.item9.bids.add(self.bid10)
        self.item9.bids.add(self.bid15)
        self.item10.bids.add(self.bid11)
        self.item10.bids.add(self.bid16)
        self.item11.bids.add(self.bid12)
        self.item11.bids.add(self.bid13)
        self.item12.bids.add(self.bid17)
        self.item12.bids.add(self.bid18)
        self.item10.claim(self.bid16)
        self.item11.claim(self.bid12)
        self.item12.claim(self.bid18)

    def test_get_items_user_has_bid_on(self):
        user1_auction2_bid_on_items = self.auction2.get_items_user_has_bid_on(self.user1)
        self.assertEqual(len(user1_auction2_bid_on_items), 3)
        self.assertEqual(self.item4 in user1_auction2_bid_on_items, True)
        self.assertEqual(self.item5 in user1_auction2_bid_on_items, True)
        self.assertEqual(self.item6 in user1_auction2_bid_on_items, True)

    def test_get_items_user_has_not_bid_on(self):
        user2_auction3_not_bid_on_items = self.auction3.get_items_user_has_not_bid_on(self.user2)
        self.assertEqual(len(user2_auction3_not_bid_on_items), 3)
        self.assertEqual(self.item8 in user2_auction3_not_bid_on_items, True)
        self.assertEqual(self.item9 in user2_auction3_not_bid_on_items, True)
        self.assertEqual(self.item14 in user2_auction3_not_bid_on_items, True)

    def test_get_items_user_is_losing(self):
        user3_auction3_items_losing = self.auction3.get_items_user_is_losing(self.user3)
        self.assertEqual(len(user3_auction3_items_losing), 2)
        self.assertEqual(self.item8 in user3_auction3_items_losing, True)
        self.assertEqual(self.item9 in user3_auction3_items_losing, True)

    def test_get_items_user_is_winning(self):
        user4_auction4_items_winning = self.auction4.get_items_user_is_winning(self.user4)
        self.assertEqual(len(user4_auction4_items_winning), 1)
        self.assertEqual(self.item10 in user4_auction4_items_winning, True)

    def test_get_sold_items(self):
        auction4_sold_items = self.auction4.get_sold_items()
        self.assertEqual(len(auction4_sold_items), 3)
        self.assertEqual(self.item10 in auction4_sold_items, True)
        self.assertEqual(self.item11 in auction4_sold_items, True)
        self.assertEqual(self.item12 in auction4_sold_items, True)

    def test_get_unsold_items(self):
        auction4_unsold_items = self.auction4.get_unsold_items()
        self.assertEqual(len(auction4_unsold_items), 1)
        self.assertEqual(self.item15 in auction4_unsold_items, True)

    def test_get_bid_count(self):
        self.assertEquals(self.auction2.bid_count, 6)

    def test_sold_item_count(self):
        self.assertEqual(self.auction4.sold_item_count, 3)

    def test_str(self):
        self.assertEqual(self.auction1.__str__(), "test1")

    def test_total_income(self):
        self.assertEqual(14, self.auction4.total_income)
        self.assertEqual(0, self.auction3.total_income)

    def test_get_bid_increment(self):
        self.assertEqual(1, self.auction1.get_bid_increment(), "Incorrect bid increment.")
