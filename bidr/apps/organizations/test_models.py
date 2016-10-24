"""
.. module:: bidr.apps.organization.test_models
   :synopsis: Bidr Silent Auction System Core Utilities Tests.

.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>
.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model
from django.test.testcases import TransactionTestCase
from django.utils import timezone

from ..auctions.models import Auction
from ..organizations.models import Organization


class OrganizationTest(TransactionTestCase):

    def setUp(self):
        # Generate users
        self.manager1 = get_user_model().objects.create_user(
            email="testmanager1@bidrapp.com", name="testmanager1", phone_number="+13105550011", password="password")
        self.manager2 = get_user_model().objects.create_user(
            email="testmanager2@bidrapp.com", name="testmanager2", phone_number="+13105550012", password="password")
        self.owner1 = get_user_model().objects.create_user(
            email="testowner1@bidrapp.com", name="testowner1", phone_number="+13105550021", password="password")

        # Generate a Organization
        self.org = Organization.objects.create(
            name="Test Studio", email="myStudio@emailaddress.com",
            phone_number="+18054523615", website="https://main.studio.com", owner=self.owner1)
        self.auction1 = Auction.objects.create(
            name="Test Auction", description="Oogalyboogaly", start_time=timezone.now(), end_time=timezone.now())
        self.auction2 = Auction.objects.create(
            name="Test Auction 2", description="Oogalyboogaly 2", start_time=timezone.now(), end_time=timezone.now())
        self.auction1.managers.add(self.manager1)
        self.auction1.managers.add(self.manager2)
        self.org.auctions.add(self.auction1)
        self.org.auctions.add(self.auction2)

    def test_organization_model(self):
        self.assertEqual(self.org.name, "Test Studio")
        self.assertEqual(self.org.email, "myStudio@emailaddress.com")
        self.assertEqual(str(self.org.phone_number), "+18054523615")
        self.assertEqual(self.org.website, "https://main.studio.com")
        self.assertNotEqual(self.org.name, "Mystudio")
        self.assertNotEqual(self.org.email, "myStudio@eaddress.com")
        self.assertNotEqual(str(self.org.phone_number), "+18054888888")
        self.assertNotEqual(self.org.website, "https://main.studio.net")

    def test_managers(self):
        self.assertEqual(self.org.managers, [self.manager1, self.manager2])

    def test_save_slug_creation(self):
        org_copy = Organization.objects.create(
            name="Test Studio", email="myStudio@emailaddress.com", phone_number="+18054523615",
            website="https://main.studio.com", owner=self.owner1)
        self.assertNotEqual(self.org.slug, org_copy.slug, "Slugs are unexpectedly equal. Should be unique")
        self.assertEqual("test-studio-2", org_copy.slug)
        org_copy_2 = Organization.objects.create(
            name="Test Studio", email="myStudio@emailaddress.com", phone_number="+18054523615",
            website="https://main.studio.com", owner=self.owner1)
        self.assertEqual("test-studio-3", org_copy_2.slug)
        org_copy_3 = Organization.objects.create(
            name="Test Studio", email="myStudio@emailaddress.com", phone_number="+18054523615",
            website="https://main.studio.com", owner=self.owner1)
        self.assertEqual("test-studio-4", org_copy_3.slug)
        org_copy_4 = Organization.objects.create(
            name="Test Studio", email="myStudio@emailaddress.com", phone_number="+18054523615",
            website="https://main.studio.com", owner=self.owner1)
        self.assertEqual("test-studio-5", org_copy_4.slug)

    def test_str(self):
        self.assertEqual(str(self.org), self.org.name)
