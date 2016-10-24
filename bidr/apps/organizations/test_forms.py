"""
.. module:: bidr.apps.organizations.test_forms
   :synopsis: Bidr Silent Auction System Organization Form Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from django.test.testcases import TestCase

from .forms import OrganizationCreateForm


class TestOrganizationCreateForm(TestCase):

    def setUp(self):
        self.request = RequestFactory()
        self.request.user = get_user_model().objects.create_user(
            "The Dude", "thedudeabides@dudeism.com", "+13107824229", "!"
        )

    def test_form_valid_all_fields(self):
        data = {
            "name": "test_name", "owner": self.request.user.id, "email": "test@email.com",
            "phone_number": "+18056413215", "website": "http://test.com"
        }
        form = OrganizationCreateForm(request=self.request, data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_mandatory_fields_with_fake_user(self):
        data = {"name": "test_name", "owner": self.request.user.id}
        form = OrganizationCreateForm(request=self.request, data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_name(self):
        data = {
            "email": "test@email.com", "owner": self.request.user.id,
            "phone_number": "+18056413215", "website": "http://test.com"
        }
        form = OrganizationCreateForm(request=self.request, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("name", form.errors)

    def test_form_valid_no_website_protocol(self):
        data = {
            "name": "test_name", "email": "test@email.com", "owner": self.request.user.id,
            "phone_number": "+18056413215", "website": "test.com"
        }
        form = OrganizationCreateForm(request=self.request, data=data)
        self.assertTrue(form.is_valid())
