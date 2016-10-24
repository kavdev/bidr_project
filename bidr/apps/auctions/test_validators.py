"""
.. module:: bidr.apps.auctions.test_validators
   :synopsis: Bidr Silent Auction System Auction Validator Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test.testcases import TestCase

from .validators import validate_user_exists


class TestValidateUserExists(TestCase):

    def setUp(self):
        # Generate Users
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

    def test_valid(self):
        self.assertEqual(None, validate_user_exists(self.user1.email))
        self.assertEqual(None, validate_user_exists(self.user2.email))

    def test_invalid(self):
        self.assertRaises(ValidationError, validate_user_exists, "testuser3@bidrapp.com")
        self.assertRaises(ValidationError, validate_user_exists, None)
        self.assertRaises(ValidationError, validate_user_exists, 2)
