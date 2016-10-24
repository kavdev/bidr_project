"""
.. module:: bidr.apps.auctions.test_managers
   :synopsis: Bidr Silent Auction System Auction Model Manager Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model
from django.test.testcases import TestCase
from django.utils import timezone

from .models import Auction


class TestManageableAuctionManager(TestCase):

    def setUp(self):
        # Generate users
        self.manager1 = get_user_model().objects.create_user(
            email="testmanager1@bidrapp.com",
            name="testmanager1",
            phone_number="+13105550011",
            password="password"
        )
        self.manager2 = get_user_model().objects.create_user(
            email="testmanager2@bidrapp.com",
            name="testmanager2",
            phone_number="+13105550012",
            password="password"
        )

        # Generate auctions
        self.auction1 = Auction.objects.create(
            name="Test Auction",
            description="Oogalyboogaly",
            start_time=timezone.now(),
            end_time=timezone.now()
        )
        self.auction2 = Auction.objects.create(
            name="Test Auction 2",
            description="Oogalyboogaly 2",
            start_time=timezone.now(),
            end_time=timezone.now()
        )
        self.auction1.managers.add(self.manager1)
        self.auction1.managers.add(self.manager2)
        self.auction2.managers.add(self.manager1)

    def test_managed_by(self):
        self.assertListEqual([self.auction1, self.auction2], list(Auction.objects.managed_by(self.manager1)))
        self.assertListEqual([self.auction1], list(Auction.objects.managed_by(self.manager2)))
