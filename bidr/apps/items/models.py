"""
.. module:: bidr.apps.items.models
   :synopsis: Bidr Silent Auction System Item Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>

"""
from django.db.models.fields import CharField, TextField, DecimalField, BooleanField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from taggit.managers import TaggableManager
from polymorphic import PolymorphicModel

from ..bids.models import Bid

class AbstractItem(PolymorphicModel):
    """ Abstract class for Items """
    
    name = CharField(max_length=60)
    description = TextField()
    claimed = BooleanField(default=False)
    claimed_bid = ForeignKey(Bid, null=True, blank=True, verbose_name="Claimed Bid")
    bids = ManyToManyField(Bid, blank=True, related_name="bids", verbose_name="Bids")
    
    def claim(self, bid):
        self.claimed = True
        self.claimed_bid = bid
        self.save()
    
    def __str__(self):
        return self.name


class Item(AbstractItem):
    """ An auction item."""

    min_price = DecimalField(max_digits=7, decimal_places=2)
    picture = ImageField()

    tags = TaggableManager()


class ItemCollection(AbstractItem):
    """ A collection of items."""

    items = ManyToManyField(Item, verbose_name="Items")
    
    def claim(self, bid):
        for item in self.items.all():
            item.claim(bid)
        super(ItemCollection, self).claim(bid)    
