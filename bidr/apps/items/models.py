"""
.. module:: bidr.apps.items.models
   :synopsis: Bidr Silent Auction System Item Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""
from django.db.models.base import Model
from django.db.models.fields import CharField, TextField, DecimalField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from ..bids.models import Bid

from taggit.managers import TaggableManager


class Item(Model):
    """ An auction item."""

    title = CharField(max_length=60)
    description = TextField()
    min_price = DecimalField(max_digits=7, decimal_places=2)
    picture = ImageField()

    bid = ForeignKey(Bid, verbose_name="Bid")

    tags = TaggableManager()


class ItemCollection(Model):
    """ A collection of items."""

    name = CharField(max_length=60)
    description = TextField()
    items = ManyToManyField(Item, verbose_name="Items")

    bid = ForeignKey(Bid, verbose_name="Bid")
