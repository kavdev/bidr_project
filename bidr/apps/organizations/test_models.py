"""
.. module:: bidr.apps.organization.test_models
   :synopsis: Bidr Silent Auction System Core Utilities Tests.

.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory

from ..auctions.models import Auction
from ..organizations.models import Organization


class OrganizationTest(TestCase):

    def setUp(self):  # noqa
        # Generate users
        self.user1 = get_user_model().objects.create_user(email="testuser1@bidrapp.com", name="testuser1", phone_number="+13105550001", password="password")
        self.user2 = get_user_model().objects.create_user(email="testuser2@bidrapp.com", name="testuser2", phone_number="+13105550002", password="password")
        self.user3 = get_user_model().objects.create_user(email="testuser3@bidrapp.com", name="testuser3", phone_number="+13105550003", password="password")
        self.user4 = get_user_model().objects.create_user(email="testuser4@bidrapp.com", name="testuser4", phone_number="+13105550004", password="password")
        self.manager1 = get_user_model().objects.create_user(email="testmanager1@bidrapp.com", name="testmanager1", phone_number="+13105550011", password="password")
        self.manager2 = get_user_model().objects.create_user(email="testmanager2@bidrapp.com", name="testmanager2", phone_number="+13105550012", password="password")
        self.manager3 = get_user_model().objects.create_user(email="testmanager3@bidrapp.com", name="testmanager3", phone_number="+13105550013", password="password")
        self.owner1 = get_user_model().objects.create_user(email="testowner1@bidrapp.com", name="testowner1", phone_number="+13105550021", password="password")
        self.owner2 = get_user_model().objects.create_user(email="testowner2@bidrapp.com", name="testowner2", phone_number="+13105550022", password="password")
        self.owner3 = get_user_model().objects.create_user(email="testowner3@bidrapp.com", name="testowner3", phone_number="+13105550023", password="password")
        self.superuser1 = get_user_model().objects.create_superuser(email="testsuperuser1@bidrapp.com", name="testsuperuser1", phone_number="+13105550031", password="password")
        self.superuser2 = get_user_model().objects.create_superuser(email="testsuperuser2@bidrapp.com", name="testsuperuser2", phone_number="+13105550032", password="password")

        # Generate a Organization
        self.org = Organization.objects.create(name="Test Studio", email="myStudio@emailaddress.com", phone_number="+18054523615", website="https://main.studio.com", owner=self.owner1)
        self.auction = Auction.objects.create(name="Test Auction", description="Oogalyboogaly", start_time=timezone.now(), end_time=timezone.now())
        self.auction2 = Auction.objects.create(name="Test Auction 2", description="Oogalyboogaly 2", start_time=timezone.now(), end_time=timezone.now())
        self.auction.managers.add(self.manager1)
        self.auction.managers.add(self.manager2)
        self.auction.save()
        self.org.auctions.add(self.auction)
        self.org.auctions.add(self.auction2)
        self.org.save()

        # set up a request
        factory = RequestFactory()
        self.request = factory.get("/")

    def test_organization_model(self):
        self.assertEqual(self.org.name, "Test Studio")
        self.assertEqual(self.org.email, "myStudio@emailaddress.com")
        self.assertEqual(str(self.org.phone_number), "+18054523615")
        self.assertEqual(self.org.website, "https://main.studio.com")
        self.assertNotEqual(self.org.name, "Mystudio")
        self.assertNotEqual(self.org.email, "myStudio@eaddress.com")
        self.assertNotEqual(str(self.org.phone_number), "+18054888888")
        self.assertNotEqual(self.org.website, "https://main.studio.net")

    def test_organization_managers(self):
        self.assertEqual(self.org.managers, [self.manager1, self.manager2])
