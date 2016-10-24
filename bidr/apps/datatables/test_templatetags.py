"""
.. module:: bidr.apps.datatables.test_templatetags
   :synopsis: Bidr Silent Auction System Datatables Template Tag and Filter Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.template.base import TemplateSyntaxError
from django.test.testcases import TestCase
from django.utils import timezone

from ..auctions.models import Auction
from ..items.ajax import PopulateBidables
from ..organizations.models import Organization
from .templatetags.datatables import do_datatables


class TestDatatables(TestCase):

    def setUp(self):
        # Generate users
        self.manager1 = get_user_model().objects.create_user(email="testmanager1@bidrapp.com", name="testmanager1", phone_number="+13105550011", password="password")
        self.manager2 = get_user_model().objects.create_user(email="testmanager2@bidrapp.com", name="testmanager2", phone_number="+13105550012", password="password")
        self.owner1 = get_user_model().objects.create_user(email="testowner1@bidrapp.com", name="testowner1", phone_number="+13105550021", password="password")

        # Generate a Organization
        self.org = Organization.objects.create(name="Test Studio", email="myStudio@emailaddress.com", phone_number="+18054523615", website="https://main.studio.com", owner=self.owner1)
        self.auction = Auction.objects.create(name="Test Auction", description="Oogalyboogaly", start_time=timezone.now(), end_time=timezone.now())
        self.auction.managers.add(self.manager1)
        self.auction.managers.add(self.manager2)
        self.org.auctions.add(self.auction)

        self.node = do_datatables(None, None)
        self.kwargs = {"auction_id": self.auction.id, "slug": self.org.slug}

    def test_datatables_script(self):
        context = {}
        context["datatables_class"] = PopulateBidables
        context["kwargs"] = self.kwargs

        self.assertIn("var datatable", self.node.render(context))

    def test_datatables_script_no_datatables_class(self):
        context = {}
        context["kwargs"] = self.kwargs

        with self.assertRaises(TemplateSyntaxError):
            self.node.render(context)

    def test_datatables_script_no_kwargs(self):
        context = {}
        context["datatables_class"] = PopulateBidables

        with self.assertRaises(TemplateSyntaxError):
            self.node.render(context)

    def test_datatables_script_datatables_class_as_none(self):
        context = {}
        context["datatables_class"] = None
        context["kwargs"] = self.kwargs

        self.assertEqual("", self.node.render(context))

    def test_datatables_script_invalid_datatables_class(self):
        context = {}
        context["datatables_class"] = TestCase  # Random class
        context["kwargs"] = self.kwargs

        with self.assertRaises(ImproperlyConfigured):
            self.node.render(context)
