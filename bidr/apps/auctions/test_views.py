"""
.. module:: bidr.apps.auctions.test_views
   :synopsis: Bidr Silent Auction System View Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from django.utils.timezone import now

from ..auctions.models import Auction, STAGES
from ..organizations.models import Organization


class TestEndAuctionView(TestCase):

    def setUp(self):
        owner = get_user_model().objects.create_superuser("The Dude", "thedudeabides@dudeism.com", "+13107824229", "!")

        self.org_instance = Organization.objects.create(name="test org", owner=owner)
        self.auction_instance = Auction.objects.create(
            name="test",
            description="test",
            start_time=now(),
            end_time=now() + timedelta(days=20)
        )

        self.org_instance.auctions.add(self.auction_instance)
        self.org_instance.save()

    def test_auction_claim_stage(self):
        self.auction_instance.stage = STAGES.index("Claim")
        self.auction_instance.save()

        self.client.login(username="thedudeabides@dudeism.com", password="!")
        response = self.client.get(reverse("end_auction", kwargs={"slug": self.org_instance.slug,
                                                                  "auction_id": self.auction_instance.id}))

        self.assertRedirects(response, reverse('auction_claim', kwargs={"slug": self.org_instance.slug,
                                                                        "auction_id": self.auction_instance.id}))

    def test_auction_report_stage(self):
        self.auction_instance.stage = STAGES.index("Report")
        self.auction_instance.save()

        self.client.login(username="thedudeabides@dudeism.com", password="!")
        response = self.client.get(reverse("end_auction", kwargs={"slug": self.org_instance.slug,
                                                                  "auction_id": self.auction_instance.id}))

        self.assertRedirects(response, reverse('auction_report', kwargs={"slug": self.org_instance.slug,
                                                                         "auction_id": self.auction_instance.id}))
