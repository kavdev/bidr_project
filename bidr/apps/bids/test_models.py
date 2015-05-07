"""
.. module:: bidr.apps.organization.test_models
   :synopsis: Bidr Silent Auction System Core Utilities Tests.

.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory

from .models import Bid


class BidTest(TestCase):

    def setUp(self):  # noqa
        # Generate users
        self.user1 = get_user_model().objects.create_user(email="testuser1@bidrapp.com", name="testuser1", phone_number="+13105550001", password="password")
        self.user2 = get_user_model().objects.create_user(email="testuser2@bidrapp.com", name="testuser2", phone_number="+13105550002", password="password")
        self.user3 = get_user_model().objects.create_user(email="testuser3@bidrapp.com", name="testuser3", phone_number="+13105550003", password="password")
        self.user4 = get_user_model().objects.create_user(email="testuser4@bidrapp.com", name="testuser4", phone_number="+13105550004", password="password")

        # Generate Bids
        self.bid1 = Bid.objects.create(amount=25, user=self.user1)
        self.bid2 = Bid.objects.create(amount=5000.24, user=self.user2)
        self.bid3 = Bid.objects.create(amount=100, user=self.user3)
        self.bid4 = Bid.objects.create(amount=6.5, user=self.user4)

        # set up a request
        factory = RequestFactory()
        self.request = factory.get("/")

    def test_bid_model(self):
        self.assertEqual(self.bid1.amount, 25)
        self.assertEqual(self.bid1.user, self.user1)
        self.assertEqual(self.bid1.__str__(), "testuser1@bidrapp.com - $25")
        self.assertEqual(self.bid2.amount, 5000.24)
        self.assertEqual(self.bid2.user, self.user2)
        self.assertEqual(self.bid2.__str__(), "testuser2@bidrapp.com - $5000.24")
        self.assertEqual(self.bid3.amount, 100)
        self.assertEqual(self.bid3.user, self.user3)
        self.assertEqual(self.bid3.__str__(), "testuser3@bidrapp.com - $100")
        self.assertEqual(self.bid4.amount, 6.5)
        self.assertEqual(self.bid4.user, self.user4)
        self.assertEqual(self.bid4.__str__(), "testuser4@bidrapp.com - $6.5")
