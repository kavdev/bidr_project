"""
.. module:: bidr.apps.auctions.models
   :synopsis: Bidr Silent Auction System Auction Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>
.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

from builtins import property
from pathlib import Path

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models.aggregates import Sum
from django.db.models.base import Model
from django.db.models.fields import CharField, TextField, DateTimeField, PositiveSmallIntegerField, BigIntegerField
from django.db.models.fields.related import ManyToManyField
from pushjack import APNSSandboxClient

from ..items.models import AbstractItem
from .managers import ManageableAuctionManager

STAGES = ["Plan", "Observe", "Claim", "Report"]
STAGE_CHOICES = [(STAGES.index(stage), stage) for stage in STAGES]


class Auction(Model):
    """ A silent auction."""

    objects = ManageableAuctionManager()

    name = CharField(max_length=60, verbose_name="Name")
    description = TextField(verbose_name="Description")
    start_time = DateTimeField(null=True, blank=True, verbose_name="Start Time")
    end_time = DateTimeField(verbose_name="End Time")
    optional_password = CharField(null=True, blank=True, verbose_name="Password", max_length=128)
    bid_increment = BigIntegerField(default=1, verbose_name="Bid Increment", validators=[MinValueValidator(1)])
    stage = PositiveSmallIntegerField(
        default=STAGES.index('Plan'),
        choices=STAGE_CHOICES,
        verbose_name="Auction Stage"
    )

    participants = ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="participants",
        verbose_name="Participants"
    )
    bidables = ManyToManyField(AbstractItem, blank=True, related_name="bidables", verbose_name="Bidables")
    managers = ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="auction_managers",
        verbose_name="Managers",
        blank=True
    )

    apns_client = APNSSandboxClient(
        certificate=str(Path(settings.STATIC_ROOT).joinpath('pem/BidrBird-ck-noenc.pem').resolve())
    )

    def get_items_user_has_bid_on(self, user_id):
        my_bids = []
        [my_bids.extend(item.bids.filter(user=user_id)) for item in self.bidables.all()]
        my_items = []
        [my_items.append(bid.bids.all()[0]) for bid in my_bids]
        return list(set(my_items))

    def get_items_user_is_winning(self, user_id):
        my_bid_items = self.get_items_user_has_bid_on(user_id)
        winning_bids = []
        [winning_bids.append(item) for item in my_bid_items if item.highest_bid.user == user_id]
        return winning_bids

    def get_items_user_is_losing(self, user_id):
        my_bid_items = self.get_items_user_has_bid_on(user_id)
        losing_bids = []
        [losing_bids.append(item) for item in my_bid_items if item.highest_bid.user != user_id]
        return losing_bids

    def get_items_user_has_not_bid_on(self, user_id):
        my_bids = self.get_items_user_has_bid_on(user_id)
        my_other_items = set(self.bidables.all()) - set(my_bids)
        return list(my_other_items)

    def get_sold_items(self):
        return self.bidables.filter(claimed=True)

    def get_unsold_items(self):
        return self.bidables.filter(claimed=False)

    @property
    def total_income(self):
        amount = self.get_sold_items().aggregate(Sum('claimed_bid__amount'))["claimed_bid__amount__sum"]
        return amount if amount else 0

    @property
    def bid_count(self):
        return sum([item.bids.all().count() for item in self.bidables.all()])

    @property
    def sold_item_count(self):
        return self.get_sold_items().count()

    def get_bid_increment(self):
        return self.bid_increment

    def __str__(self):
        return self.name
