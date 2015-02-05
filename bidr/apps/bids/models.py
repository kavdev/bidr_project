"""
.. module:: bidr.apps.bids.models
   :synopsis: Bidr Silent Auction System Bid Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.db.models.base import Model
from django.db.models.fields import DecimalField, DateTimeField
from django.db.models.fields.related import ForeignKey
from django.conf import settings


class Bid(Model):
    """A bid on an item."""

    amount = DecimalField(max_digits=40, decimal_places=2, verbose_name='Bid Amount')
    user = ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Bidder')
    timestamp = DateTimeField(auto_now_add=True, blank=True, verbose_name='Timestamp')

    def __str__(self):
        return str(self.user) + " - $" + str(self.amount)
