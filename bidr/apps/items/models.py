"""
.. module:: bidr.apps.items.models
   :synopsis: Bidr Silent Auction System Item Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>

"""

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.validators import MinValueValidator
from django.db.models.fields import CharField, TextField, DecimalField, BooleanField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.aggregates import Max, Sum

from taggit.managers import TaggableManager
from polymorphic import PolymorphicModel

from ..bids.models import Bid


class AbstractItem(PolymorphicModel):
    """ Abstract class for Items """

    name = CharField(max_length=60)
    description = TextField(blank=True, max_length=300)
    claimed = BooleanField(default=False)
    claimed_bid = ForeignKey(Bid, null=True, blank=True, verbose_name="Claimed Bid")
    bids = ManyToManyField(Bid, blank=True, related_name="bids", verbose_name="Bids")

    def claim(self, bid):
        self.claimed = True
        self.claimed_bid = bid
        self.save()

    def get_second_highest_bid(self):
        bid_list = self.bids.all().order_by("-amount")
        if bid_list.count() > 1:
            return bid_list[1]
        else:
            return None

    def __str__(self):
        return self.name

    def get_bids_by_amount(self):
        return self.bids.all().order_by("-amount")

    @property
    def image_urls(self):
        raise NotImplementedError("Subclasses should implement this!")

    @property
    def highest_bid(self):
        """ This only works because no bid can have the same amount."""

        highest_amount = self.bids.all().aggregate(Max('amount'))["amount__max"]
        if not highest_amount:
            return None
        return self.bids.get(amount=highest_amount)

    @property
    def min_price(self):
        raise NotImplementedError("Subclasses should implement this!")

    @property
    def polymorphic_identifier(self):
        return self.polymorphic_ctype.name


class Item(AbstractItem):
    """ An auction item."""

    minimum_price = DecimalField(max_digits=7, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    picture = ImageField(null=True, blank=True)

    tags = TaggableManager()

    def _image_url(self):
        if self.picture:
            return self.picture.url
        else:
            return static('img/no_image.png')

    @property
    def image_urls(self):
        return [self._image_url()]

    @property
    def min_price(self):
        return self.minimum_price


class ItemCollection(AbstractItem):
    """ A collection of items."""

    items = ManyToManyField(Item, blank=True, verbose_name="Items")

    def claim(self, bid):
        for item in self.items.all():
            item.claim(bid)
        super(ItemCollection, self).claim(bid)

    @property
    def image_urls(self):
        return [x._image_url() for x in self.items.all()[:4]]

    @property
    def min_price(self):
        return self.items.aggregate(Sum('minimum_price'))["minimum_price__sum"]

    @property
    def ordered_items(self):
        return self.items.all().order_by("name")
