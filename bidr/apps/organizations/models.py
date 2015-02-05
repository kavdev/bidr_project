"""
.. module:: bidr.apps.bids.models
   :synopsis: Bidr Silent Auction System Bid Models.

.. moduleauthor:: Jirbert Dilanchian <Jirbert@gmail.com>

"""

from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.conf import settings
from ..auctions.models import Auction


class Organization(Model):
    """An Organization that manages silent auction."""

    name = CharField(max_length=100, verbose_name="Name")
    owner = ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Admin")
    managers = ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Manager")
    auctions = ManyToManyField(Auction)

    def __str__(self):
        return self.name
