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

    def setUp(self):
        # Generate users
        self.user1 = get_user_model().objects.create_user(email="testuser1@bidrapp.com", name="testuser1", phone_number="+13105550001", password="password")
        self.manager1 = get_user_model().objects.create_user(email="testmanager1@bidrapp.com", name="testmanager1", phone_number="+13105550011", password="password")
        self.owner1 = get_user_model().objects.create_user(email="testowner1@bidrapp.com", name="testowner1", phone_number="+13105550021", password="password")
        self.superuser1 = get_user_model().objects.create_superuser(email="testsuperuser1@bidrapp.com", name="testsuperuser1", phone_number="+13105550031", password="password")

        # Generate a Organization
        self.org = Organization.objects.create(name="Test Studio", email="myStudio@emailaddress.com", phone_number="+18054523615", website="https://main.studio.com", owner=self.owner1)
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
