"""
.. module:: bidr.apps.core.test_views
   :synopsis: Bidr Silent Auction System View Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from django.utils.encoding import smart_str


class TestIndexView(TestCase):

    def test_get(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(200, response.status_code, "Response not success")

        # Check page content
        self.assertIn("Bidr Silent Auction System", smart_str(response.content))
        self.assertIn("A silent auction system for the digital age", smart_str(response.content))
        self.assertIn("""<form name="registration_form" method="POST" id="registration_form">""", smart_str(response.content))

    def test_post_redirects_to_home(self):
        response = self.client.post(reverse("home"), data={"name": "test",
                                                           "email": "test@test.com",
                                                           "phone_number": "+13102792299",
                                                           "password": "test1234",
                                                           "password_confirm": "test1234"})
        self.assertRedirects(response, reverse("home"))
