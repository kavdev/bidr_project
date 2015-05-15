"""
.. module:: bidr.apps.core.test_forms
   :synopsis: Bidr Silent Auction System Core Form Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.test.testcases import TestCase

from .forms import UserRegistrationForm
from django.contrib.auth import get_user_model


class TestUserRegistrationForm(TestCase):

    def setUp(self):  # noqa
        self.user = get_user_model().objects.create(name="test", email="popularemail@test.com", phone_number="12345456656", password="!")

    def test_form_valid(self):
        data = {"name": "test_name",
                "email": "test_email@email.com",
                "phone_number": "+13105551987",
                "password": "bidr2015", "password_confirm": "bidr2015"}
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_display_name(self):
        data = {"name": "test_name",
                "display_name": "Display Name",
                "email": "test_email@email.com",
                "phone_number": "+13105551987",
                "password": "bidr2015", "password_confirm": "bidr2015"}
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_email_already_in_use(self):
        data = {"name": "test_name",
                "email": "popularemail@test.com",
                "phone_number": "+13105551987",
                "password": "bidr2015", "password_confirm": "bidr2015"}
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("email", form.errors)

    def test_form_invalid_mismatched_passwords(self):
        data = {"name": "test_name",
                "email": "test_email@email.com",
                "phone_number": "+13105551987",
                "password": "bidr2015", "password_confirm": "bidr2016"}
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.non_field_errors()))

    def test_form_invalid_missing_password(self):
        data = {"name": "test_name",
                "email": "test_email@email.com",
                "phone_number": "+13105551987", "password_confirm": "bidr2015"}
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("password", form.errors)

    def test_form_invalid_missing_password_confirm(self):
        data = {"name": "test_name",
                "email": "test_email@email.com",
                "phone_number": "+13105551987", "password": "bidr2015"}
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("password_confirm", form.errors)
