"""
.. module:: bidr.apps.core.test_managers
   :synopsis: Bidr Silent Auction System Core Model Manager Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model
from django.test.testcases import TestCase


class TestBidrUserManager(TestCase):

    def test_create_user(self):
        get_user_model().objects.create_user(
            name="test_name",
            email="testemail@test.com",
            phone_number="1234252345",
            password="!"
        )

    def test_create_user_missing_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                name="test_name",
                email=None,
                phone_number="1234252345",
                password="!"
            )

    def test_create_superuser(self):
        get_user_model().objects.create_superuser(
            name="test_name",
            email="testemail@test.com",
            phone_number="1234252345",
            password="!"
        )
