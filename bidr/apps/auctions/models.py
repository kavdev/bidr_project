"""
.. module:: bidr.apps.auctions.models
   :synopsis: Bidr Silent Auction System Auction Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>

"""

from django.conf import settings
from django.db.models.aggregates import Sum
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.fields import CharField, TextField, DateTimeField, PositiveSmallIntegerField

from ..items.models import AbstractItem
from .managers import ManageableAuctionManager


class AuctionUserInfo(Model):
    """ Additional user fields defined for a particular auction."""

    bidder = ForeignKey(settings.AUTH_USER_MODEL)
    attribute_name = CharField(max_length=60)
    attribute_value = CharField(max_length=100)


STAGES = ["Plan", "Observe", "Claim", "Report"]
STAGE_CHOICES = [(STAGES.index(stage), stage) for stage in STAGES]


class Auction(Model):
    """ A silent auction."""

    objects = ManageableAuctionManager()

    name = CharField(max_length=60, verbose_name="Name")
    description = TextField(verbose_name="Description")
    end_time = DateTimeField(verbose_name="End Time")
    optional_password = CharField(null=True, blank=True, verbose_name="Password", max_length=128)
    stage = PositiveSmallIntegerField(default=STAGES.index('Plan'), choices=STAGE_CHOICES, verbose_name="Auction Stage")

    bidables = ManyToManyField(AbstractItem, blank=True, related_name="bidables", verbose_name="Bidables")

    user_info = ManyToManyField(AuctionUserInfo, blank=True, verbose_name="Additional User Info")

    managers = ManyToManyField(settings.AUTH_USER_MODEL, related_name="auction_managers", verbose_name="Managers", blank=True)

    def get_sold_items(self):
        return self.bidables.filter(claimed=True)

    def get_unsold_items(self):
        return self.bidables.filter(claimed=False)

    @property
    def total_income(self):
        return self.get_sold_items().aggregate(Sum('claimed_bid__amount'))["claimed_bid__amount__sum"]

    @property
    def bid_count(self):
        return sum([item.bids.all().count() for item in self.bidables.all()])

    @property
    def sold_item_count(self):
        return self.get_sold_items().count()

    def __str__(self):
        return self.name
