"""
.. module:: bidr.apps.organization.test_models
   :synopsis: Bidr Silent Auction System Core Utilities Tests.

.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>
.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now, make_aware

from ..bids.models import Bid


class BidTest(TestCase):

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
        self.bid0 = Bid.objects.create(amount=20, user=self.user1)
        self.bid1 = Bid.objects.create(amount=25, user=self.user1)
        self.bid2 = Bid.objects.create(amount=5000, user=self.user2)
        self.bid3 = Bid.objects.create(amount=100, user=self.user3)
        self.bid4 = Bid.objects.create(amount=6, user=self.user4)
        self.bid5 = Bid.objects.create(amount=25, user=self.user3)
        self.bid6 = Bid.objects.create(amount=0, user=self.user2)

        self.bid0.timestamp = now() - timedelta(minutes=1)
        self.bid0.save()
        self.bid1.timestamp = now() - timedelta(minutes=20)
        self.bid1.save()
        self.bid2.timestamp = now() - timedelta(hours=1, minutes=20)
        self.bid2.save()
        self.bid3.timestamp = now() - timedelta(hours=2, minutes=20)
        self.bid3.save()
        self.bid4.timestamp = now() - timedelta(hours=3, minutes=20)
        self.bid4.save()
        self.bid6.timestamp = make_aware(datetime(2015, 5, 11, 12, 30)) - timedelta(hours=22, minutes=15)
        self.bid6.save()

    def test_bid_model(self):
        self.assertEqual(self.bid1.amount, 25)
        self.assertEqual(self.bid1.user, self.user1)
        self.assertEqual(str(self.bid1), "testuser1@bidrapp.com - $25")
        self.assertEqual(self.bid2.amount, 5000)
        self.assertEqual(self.bid2.user, self.user2)
        self.assertEqual(str(self.bid2), "testuser2@bidrapp.com - $5000")
        self.assertEqual(self.bid3.amount, 100)
        self.assertEqual(self.bid3.user, self.user3)
        self.assertEqual(str(self.bid3), "testuser3@bidrapp.com - $100")
        self.assertEqual(self.bid4.amount, 6)
        self.assertEqual(self.bid4.user, self.user4)
        self.assertEqual(str(self.bid4), "testuser4@bidrapp.com - $6")

    def test_time_delta(self):
        self.assertEqual(self.bid0.time_delta(), "1 minute ago")
        self.assertEqual(self.bid1.time_delta(), "20 minutes ago")
        self.assertEqual(self.bid2.time_delta(), "1 hour ago")
        self.assertEqual(self.bid3.time_delta(), "2 hours ago")
        self.assertEqual(self.bid4.time_delta(), "3 hours ago")
        self.assertEqual(self.bid6.time_delta(), "2015-05-10  14:15")
