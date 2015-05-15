"""
.. module:: bidr.apps.core.test_models
   :synopsis: Bidr Silent Auction System Core Model Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model
from django.core import mail
from django.test.testcases import TestCase


class TestBidrUser(TestCase):

    def setUp(self):  # noqa
        self.user = get_user_model().objects.create(name="test", email="popularemail@test.com", phone_number="12345456656", password="!")

    def test_get_full_name(self):
        self.assertEqual("test", self.user.get_full_name())

    def test_get_display_name(self):
        self.assertEqual("Anonymous", self.user.get_display_name())

    def test_get_short_name(self):
        self.assertEqual("popularemail@test.com", self.user.get_short_name())

    def test_email_user(self):
        mail.outbox = []

        self.user.email_user(subject="test_subject", message="test_message")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test_subject')
        self.assertEqual(mail.outbox[0].body, 'test_message')
        self.assertEqual(mail.outbox[0].to, [self.user.email])
