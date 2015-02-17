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

    bid = ForeignKey(Bid, verbose_name="Bid")
    
    def claim(self):
        self.claimed = True
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
    
    def claim(self):
        for item in self.items.all():
            item.claim()
        super(ItemCollection, self).claim()    
