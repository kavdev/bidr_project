"""
.. module:: bidr.apps.core.test_utils
   :synopsis: Bidr Silent Auction System Core Utilities Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from unittest.mock import Mock

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory

from ..auctions.models import Auction
from ..organizations.models import Organization
from .utils import UserType, user_is_type, user_type_test


class UserTypeTest(TestCase):

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
        self.org = Organization.objects.create(name="Test Studio", owner=self.owner1)
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

    def test_superuser_type(self):
        self.assertTrue(user_type_test(user_type=UserType.SUPERUSER, user=self.superuser1, org_slug=self.org.slug), "Valid Superuser")

        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.user1, org_slug=self.org.slug), "user1")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.user2, org_slug=self.org.slug), "user2")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.user3, org_slug=self.org.slug), "user3")

        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.manager1, org_slug=self.org.slug), "manager1")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.manager2, org_slug=self.org.slug), "manager2")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.manager3, org_slug=self.org.slug), "manager3")

        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.owner1, org_slug=self.org.slug), "owner1")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.owner2, org_slug=self.org.slug), "owner2")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.owner3, org_slug=self.org.slug), "owner3")

    def test_superuser_type_with_auction_id(self):
        self.assertTrue(user_type_test(user_type=UserType.SUPERUSER, user=self.superuser1, org_slug=self.org.slug, auction_id=self.auction.id), "Valid Superuser")

        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.user1, org_slug=self.org.slug, auction_id=self.auction.id), "user1")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.user2, org_slug=self.org.slug, auction_id=self.auction.id), "user2")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.user3, org_slug=self.org.slug, auction_id=self.auction.id), "user3")

        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.manager1, org_slug=self.org.slug, auction_id=self.auction.id), "manager1")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.manager2, org_slug=self.org.slug, auction_id=self.auction.id), "manager2")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.manager3, org_slug=self.org.slug, auction_id=self.auction.id), "manager3")

        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.owner1, org_slug=self.org.slug, auction_id=self.auction.id), "owner1")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.owner2, org_slug=self.org.slug, auction_id=self.auction.id), "owner2")
        self.assertFalse(user_type_test(user_type=UserType.SUPERUSER, user=self.owner3, org_slug=self.org.slug, auction_id=self.auction.id), "owner3")

    def test_superuser_type_via_request(self):
        self.assertTrue(self._test_user_via_request(user_type=UserType.SUPERUSER, user=self.superuser1), "Valid Superuser")

        self.assertFalse(self._test_user_via_request(user_type=UserType.SUPERUSER, user=self.user1), "user1")
        self.assertFalse(self._test_user_via_request(user_type=UserType.SUPERUSER, user=self.user2), "user2")
        self.assertFalse(self._test_user_via_request(user_type=UserType.SUPERUSER, user=self.user3), "user3")

        self.assertFalse(self._test_user_via_request(user_type=UserType.SUPERUSER, user=self.manager1), "manager1")
        self.assertFalse(self._test_user_via_request(user_type=UserType.SUPERUSER, user=self.manager2), "manager2")
        self.assertFalse(self._test_user_via_request(user_type=UserType.SUPERUSER, user=self.manager3), "manager3")

        self.assertFalse(self._test_user_via_request(user_type=UserType.SUPERUSER, user=self.owner1), "owner1")
        self.assertFalse(self._test_user_via_request(user_type=UserType.SUPERUSER, user=self.owner2), "owner2")
        self.assertFalse(self._test_user_via_request(user_type=UserType.SUPERUSER, user=self.owner3), "owner3")

    def test_owner_type(self):
        self.assertTrue(user_type_test(user_type=UserType.OWNER, user=self.owner1, org_slug=self.org.slug), "Valid Owner")
        self.assertTrue(user_type_test(user_type=UserType.OWNER, user=self.superuser1, org_slug=self.org.slug), "Valid Superuser")

        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.user1, org_slug=self.org.slug), "user1")
        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.user2, org_slug=self.org.slug), "user2")
        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.user3, org_slug=self.org.slug), "user3")

        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.manager1, org_slug=self.org.slug), "manager1")
        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.manager2, org_slug=self.org.slug), "manager2")
        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.manager3, org_slug=self.org.slug), "manager3")

        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.owner2, org_slug=self.org.slug), "owner2")
        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.owner3, org_slug=self.org.slug), "owner3")

    def test_owner_type_with_auction_id(self):
        self.assertTrue(user_type_test(user_type=UserType.OWNER, user=self.owner1, org_slug=self.org.slug, auction_id=self.auction.id), "Valid Owner")
        self.assertTrue(user_type_test(user_type=UserType.OWNER, user=self.superuser1, org_slug=self.org.slug, auction_id=self.auction.id), "Valid Superuser")

        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.user1, org_slug=self.org.slug, auction_id=self.auction.id), "user1")
        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.user2, org_slug=self.org.slug, auction_id=self.auction.id), "user2")
        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.user3, org_slug=self.org.slug, auction_id=self.auction.id), "user3")

        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.manager1, org_slug=self.org.slug, auction_id=self.auction.id), "manager1")
        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.manager2, org_slug=self.org.slug, auction_id=self.auction.id), "manager2")
        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.manager3, org_slug=self.org.slug, auction_id=self.auction.id), "manager3")

        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.owner2, org_slug=self.org.slug, auction_id=self.auction.id), "owner2")
        self.assertFalse(user_type_test(user_type=UserType.OWNER, user=self.owner3, org_slug=self.org.slug, auction_id=self.auction.id), "owner3")

    def test_owner_type_via_request(self):
        self.assertTrue(self._test_user_via_request(user_type=UserType.OWNER, user=self.owner1), "Valid Owner")
        self.assertTrue(self._test_user_via_request(user_type=UserType.OWNER, user=self.superuser1), "Valid Superuser")

        self.assertFalse(self._test_user_via_request(user_type=UserType.OWNER, user=self.user1), "user1")
        self.assertFalse(self._test_user_via_request(user_type=UserType.OWNER, user=self.user2), "user2")
        self.assertFalse(self._test_user_via_request(user_type=UserType.OWNER, user=self.user3), "user3")

        self.assertFalse(self._test_user_via_request(user_type=UserType.OWNER, user=self.manager1), "manager1")
        self.assertFalse(self._test_user_via_request(user_type=UserType.OWNER, user=self.manager2), "manager2")
        self.assertFalse(self._test_user_via_request(user_type=UserType.OWNER, user=self.manager3), "manager3")

        self.assertFalse(self._test_user_via_request(user_type=UserType.OWNER, user=self.owner2), "owner2")
        self.assertFalse(self._test_user_via_request(user_type=UserType.OWNER, user=self.owner3), "owner3")

    def test_manager_type(self):
        self.assertTrue(user_type_test(user_type=UserType.MANAGER, user=self.owner1, org_slug=self.org.slug), "Valid Owner")
        self.assertTrue(user_type_test(user_type=UserType.MANAGER, user=self.superuser1, org_slug=self.org.slug), "Valid Superuser")
        self.assertTrue(user_type_test(user_type=UserType.MANAGER, user=self.manager1, org_slug=self.org.slug), "Valid manager1")
        self.assertTrue(user_type_test(user_type=UserType.MANAGER, user=self.manager2, org_slug=self.org.slug), "Valid manager2")

        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.user1, org_slug=self.org.slug), "user1")
        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.user2, org_slug=self.org.slug), "user2")
        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.user3, org_slug=self.org.slug), "user3")

        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.manager3, org_slug=self.org.slug), "manager3")

        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.owner2, org_slug=self.org.slug), "owner2")
        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.owner3, org_slug=self.org.slug), "owner3")

    def test_manager_type_with_auction_id(self):
        self.assertTrue(user_type_test(user_type=UserType.MANAGER, user=self.owner1, org_slug=self.org.slug, auction_id=self.auction.id), "Valid Owner")
        self.assertTrue(user_type_test(user_type=UserType.MANAGER, user=self.superuser1, org_slug=self.org.slug, auction_id=self.auction.id), "Valid Superuser")
        self.assertTrue(user_type_test(user_type=UserType.MANAGER, user=self.manager1, org_slug=self.org.slug, auction_id=self.auction.id), "Valid manager1")
        self.assertTrue(user_type_test(user_type=UserType.MANAGER, user=self.manager2, org_slug=self.org.slug, auction_id=self.auction.id), "Valid manager2")

        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.manager1, org_slug=self.org.slug, auction_id=self.auction2.id), "Valid manager1")
        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.manager2, org_slug=self.org.slug, auction_id=self.auction2.id), "Valid manager2")

        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.user1, org_slug=self.org.slug, auction_id=self.auction.id), "user1")
        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.user2, org_slug=self.org.slug, auction_id=self.auction.id), "user2")
        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.user3, org_slug=self.org.slug, auction_id=self.auction.id), "user3")

        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.manager3, org_slug=self.org.slug, auction_id=self.auction.id), "manager3")

        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.owner2, org_slug=self.org.slug, auction_id=self.auction.id), "owner2")
        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.owner3, org_slug=self.org.slug, auction_id=self.auction.id), "owner3")

    def test_manager_type_via_request(self):
        self.assertTrue(self._test_user_via_request(user_type=UserType.MANAGER, user=self.owner1), "Valid Owner")
        self.assertTrue(self._test_user_via_request(user_type=UserType.MANAGER, user=self.superuser1), "Valid Superuser")
        self.assertTrue(self._test_user_via_request(user_type=UserType.MANAGER, user=self.manager1), "Valid manager1")
        self.assertTrue(self._test_user_via_request(user_type=UserType.MANAGER, user=self.manager2), "Valid manager2")

        self.assertFalse(self._test_user_via_request(user_type=UserType.MANAGER, user=self.user1), "user1")
        self.assertFalse(self._test_user_via_request(user_type=UserType.MANAGER, user=self.user2), "user2")
        self.assertFalse(self._test_user_via_request(user_type=UserType.MANAGER, user=self.user3), "user3")

        self.assertFalse(self._test_user_via_request(user_type=UserType.MANAGER, user=self.manager3), "manager3")

        self.assertFalse(self._test_user_via_request(user_type=UserType.MANAGER, user=self.owner2), "owner2")
        self.assertFalse(self._test_user_via_request(user_type=UserType.MANAGER, user=self.owner3), "owner3")

    def test_unknown_type(self):
        self.assertFalse(user_type_test(user_type=-1, user=self.superuser1, org_slug=self.org.slug), "superuser unknown")
        self.assertFalse(user_type_test(user_type=-1, user=self.owner1, org_slug=self.org.slug), "owner1 unknown")
        self.assertFalse(user_type_test(user_type=-1, user=self.owner3, org_slug=self.org.slug), "owner3 unknown")

    def test_unknown_type_with_auction_id(self):
        self.assertFalse(user_type_test(user_type=-1, user=self.superuser1, org_slug=self.org.slug, auction_id=self.auction.id), "superuser unknown")
        self.assertFalse(user_type_test(user_type=-1, user=self.owner1, org_slug=self.org.slug, auction_id=self.auction.id), "owner1 unknown")
        self.assertFalse(user_type_test(user_type=-1, user=self.owner3, org_slug=self.org.slug, auction_id=self.auction.id), "owner3 unknown")

    def test_unknown_type_via_request(self):
        self.assertFalse(self._test_user_via_request(user_type=-1, user=self.superuser1), "superuser unknown")
        self.assertFalse(self._test_user_via_request(user_type=-1, user=self.owner1), "owner1 unknown")
        self.assertFalse(self._test_user_via_request(user_type=-1, user=self.owner3), "owner3 unknown")

    def test_uncached_user(self):
        self.assertFalse(user_type_test(user_type=UserType.MANAGER, user=self.user4, org_slug=self.org.slug), "User4 incorrectly treated as an instructior.")

    def test_uncached_superuser_via_request(self):
        self.assertTrue(self._test_user_via_request(user_type=UserType.SUPERUSER, user=self.superuser2), "Valid Superuser")

    def test_bad_function_call(self):
        self.assertRaises(TypeError, user_type_test, user_type=UserType.MANAGER, user=self.user1)

    def _test_user_via_request(self, user_type, user):
        self.request.user = user

        expected_response = "Kalamazoo"

        view = Mock(return_value=expected_response)
        decorated_func = user_is_type(user_type)(view)
        response = decorated_func(self.request, slug=self.org.slug)

        if view.called:
            view.assert_called_with(self.request, slug=self.org.slug)
            self.assertEqual(expected_response, response, "Mock view's return value is incorrect.")
            return True
        else:
            # Redirected to login
            return False
