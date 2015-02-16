"""
.. module:: bidr.apps.auctions.models
   :synopsis: Bidr Silent Auction System Auction Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.conf import settings
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.fields import CharField, TextField, DateTimeField, PositiveSmallIntegerField

from ..items.models import Item, ItemCollection
from .managers import ManageableAuctionManager


class AuctionUserInfo(Model):
    """ Additional user fields defined for a particular auction."""

    bidder = ForeignKey(settings.AUTH_USER_MODEL)
    attribute_name = CharField(max_length=60)
    attribute_value = CharField(max_length=100)


STAGES = ["Plan", "Manage", "Claim", "Report"]
STAGE_CHOICES = [(STAGES.index(stage), stage) for stage in STAGES]


class Auction(Model):
    """ A silent auction."""

    objects = ManageableAuctionManager()

    name = CharField(max_length=60, verbose_name="Name")
    description = TextField(verbose_name="Description")
    start_time = DateTimeField(verbose_name="Start Time")
    end_time = DateTimeField(verbose_name="End Time")
    optional_password = CharField(null=True, blank=True, verbose_name="Password", max_length=128)
    stage = PositiveSmallIntegerField(default=STAGES.index('Plan'), choices=STAGE_CHOICES, verbose_name="Auction Stage")

    items = ManyToManyField(Item, blank=True, verbose_name="Items")
    item_collections = ManyToManyField(ItemCollection, blank=True, verbose_name="Collections of Items")

    user_info = ManyToManyField(AuctionUserInfo, blank=True, verbose_name="Additional User Info")

    managers = ManyToManyField(settings.AUTH_USER_MODEL, related_name="auction_managers", verbose_name="Managers", blank=True)

    def __str__(self):
        return self.name
