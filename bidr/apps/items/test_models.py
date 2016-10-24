"""
.. module:: bidr.apps.items.test_models
   :synopsis: Bidr Silent Auction System Item Model Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from unittest.mock import MagicMock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.test.testcases import TestCase
from django.utils import timezone

from ..auctions.models import Auction
from ..bids.models import Bid
from .models import Item, ItemCollection, AbstractItem


class TestAbstractItem(TestCase):

    def setUp(self):
        self.abstract_item_instance = AbstractItem.objects.create(name="test_name", description="test_description")

    def test_image_urls(self):
        with self.assertRaises(NotImplementedError):
            self.abstract_item_instance.image_urls

    def test_total_starting_bid(self):
        with self.assertRaises(NotImplementedError):
            self.abstract_item_instance.total_starting_bid


class TestItem(TestCase):

    def setUp(self):
        self.auction_instance = Auction.objects.create(name="Test Auction", description="Oogalyboogaly", start_time=timezone.now(), end_time=timezone.now())
        self.item_instance = Item.objects.create(name="test_item", description="test_description", starting_bid=2)
        self.item_instance_no_bids = Item.objects.create(name="test_item2", description="test_description", starting_bid=2)

        self.auction_instance.bidables.add(self.item_instance_no_bids)
        self.auction_instance.bidables.add(self.item_instance)

        # Generate Users
        self.user1 = get_user_model().objects.create_user(email="testuser1@bidrapp.com", name="testuser1", phone_number="+13105550001", password="password")
        self.user2 = get_user_model().objects.create_user(email="testuser2@bidrapp.com", name="testuser2", phone_number="+13105550002", password="password")
        self.user3 = get_user_model().objects.create_user(email="testuser3@bidrapp.com", name="testuser3", phone_number="+13105550003", password="password")
        self.user4 = get_user_model().objects.create_user(email="testuser4@bidrapp.com", name="testuser4", phone_number="+13105550004", password="password")

        # Generate Bids
        self.bid1 = Bid.objects.create(amount=1, user=self.user1)
        self.bid2 = Bid.objects.create(amount=5, user=self.user2)
        self.bid3 = Bid.objects.create(amount=7, user=self.user2)
        self.bid4 = Bid.objects.create(amount=2, user=self.user3)
        self.bid5 = Bid.objects.create(amount=4, user=self.user3)
        self.bid6 = Bid.objects.create(amount=6, user=self.user3)
        self.bid7 = Bid.objects.create(amount=3, user=self.user4)
        self.bid8 = Bid.objects.create(amount=8, user=self.user4)

        # Add bids to the item
        self.item_instance.bids.add(self.bid1)
        self.item_instance.bids.add(self.bid2)
        self.item_instance.bids.add(self.bid3)
        self.item_instance.bids.add(self.bid4)
        self.item_instance.bids.add(self.bid5)
        self.item_instance.bids.add(self.bid6)
        self.item_instance.bids.add(self.bid7)
        self.item_instance.bids.add(self.bid8)

    def test_image_urls_no_image(self):
        self.assertIn(static('img/no_image.png'), self.item_instance.image_urls, "Incorrect image url list for no image.")

    def test_image_urls_image_exists(self):
        self.item_instance.picture = MagicMock(url="test_url")
        self.assertIn("test_url", self.item_instance.image_urls, "Incorrect image url list for existing image.")

    def test_total_starting_bid(self):
        self.assertEqual(2, self.item_instance.total_starting_bid, "Incorrect starting bid.")

    def test_polymorphic_identifier(self):
        self.assertEqual("item", self.item_instance.polymorphic_identifier)

    def test_bidders(self):
        self.assertEquals(len(self.item_instance.bidders), 4)
        self.assertTrue(self.user1 in self.item_instance.bidders)
        self.assertTrue(self.user2 in self.item_instance.bidders)
        self.assertTrue(self.user3 in self.item_instance.bidders)
        self.assertTrue(self.user4 in self.item_instance.bidders)

    def test_str(self):
        self.assertEqual("test_item", str(self.item_instance))

    def test_highest_bid(self):
        self.assertEqual(self.bid8, self.item_instance.highest_bid)

    def test_second_highest_bid(self):
        self.assertEqual(self.bid3, self.item_instance.get_second_highest_bid())
        self.assertEqual(None, self.item_instance_no_bids.get_second_highest_bid())

    def test_get_bids_by_amount(self):
        self.assertListEqual([self.bid8, self.bid3, self.bid6, self.bid2, self.bid5, self.bid7, self.bid4, self.bid1], list(self.item_instance.get_bids_by_amount()))

    def test_get_previous_bid_by_user(self):
        self.assertEqual(self.bid7, self.item_instance.get_previous_bid_by_user(self.user4))
        self.assertEqual(self.bid5, self.item_instance.get_previous_bid_by_user(self.user3))
        self.assertEqual(self.bid2, self.item_instance.get_previous_bid_by_user(self.user2))
        self.assertEqual(None, self.item_instance.get_previous_bid_by_user(self.user1))

    def test_get_absolute_client_url(self):
        request = RequestFactory()

        url_base = "https://bidrapp.com"
        auction_id = self.auction_instance.id
        item_id = self.item_instance.id

        request.build_absolute_uri = (lambda location: url_base + location)

        absolute_url = self.item_instance.get_absolute_client_url(request)

        self.assertEqual(url_base + reverse("client:item_detail", kwargs={"auction_id": auction_id, "pk": item_id}), absolute_url)


class TestItemCollection(TestCase):

    def setUp(self):
        self.item_instance_1 = Item.objects.create(name="Xtest_item_1", description="test_description", starting_bid=2, picture='test_url_1')
        self.item_instance_2 = Item.objects.create(name="Ctest_item_2", description="test_description", starting_bid=4, picture='test_url_2')
        self.item_instance_3 = Item.objects.create(name="Ftest_item_3", description="test_description", starting_bid=6, picture='test_url_3')
        self.item_instance_4 = Item.objects.create(name="Qtest_item_4", description="test_description", starting_bid=8, picture='test_url_4')
        self.item_instance_5 = Item.objects.create(name="Atest_item_5", description="test_description", starting_bid=10, picture='test_url_5')

        self.item_instance_1.tags.add("tag1")
        self.item_instance_1.tags.add("tag1")
        self.item_instance_1.tags.add("tag2")
        self.item_instance_2.tags.add("tag2")
        self.item_instance_3.tags.add("tag3")
        self.item_instance_3.tags.add("tag5")
        self.item_instance_4.tags.add("tag4")
        self.item_instance_5.tags.add("tag5")

        self.collection_instance = ItemCollection.objects.create(name="colleciton_1", description="test_description")
        self.collection_instance.items.add(self.item_instance_1)
        self.collection_instance.items.add(self.item_instance_2)
        self.collection_instance.items.add(self.item_instance_3)
        self.collection_instance.items.add(self.item_instance_4)
        self.collection_instance.items.add(self.item_instance_5)

    def test_image_urls(self):
        self.assertIn(settings.MEDIA_URL + "test_url_1", self.collection_instance.image_urls, "Picture 1 not in image url list.")
        self.assertIn(settings.MEDIA_URL + "test_url_2", self.collection_instance.image_urls, "Picture 2 not in image url list.")
        self.assertIn(settings.MEDIA_URL + "test_url_3", self.collection_instance.image_urls, "Picture 3 not in image url list.")
        self.assertIn(settings.MEDIA_URL + "test_url_4", self.collection_instance.image_urls, "Picture 4 not in image url list.")

        self.assertNotIn(settings.MEDIA_URL + "test_url_5", self.collection_instance.image_urls, "Picture 5 unexpectedly in image url list. List should only contain first four images.")

    def test_total_starting_bid(self):
        self.assertEqual(30, self.collection_instance.total_starting_bid, "Incorrect starting bid.")

    def test_ordered_items(self):
        item_list = list(self.collection_instance.ordered_items.values_list('name', flat=True))

        self.assertListEqual(["Atest_item_5", "Ctest_item_2", "Ftest_item_3", "Qtest_item_4", "Xtest_item_1"], item_list)

    def test_tags(self):
        self.assertListEqual(["tag1", "tag2", "tag3", "tag4", "tag5"], sorted(self.collection_instance.tags), "Tags don't match.")

    def test_polymorphic_identifier(self):
        self.assertEqual("item collection", self.collection_instance.polymorphic_identifier)

    def test_str(self):
        self.assertEqual("colleciton_1", str(self.collection_instance))
