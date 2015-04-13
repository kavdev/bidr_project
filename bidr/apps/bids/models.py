"""
.. module:: bidr.apps.bids.models
   :synopsis: Bidr Silent Auction System Bid Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.db.models.base import Model
from django.db.models.fields import DecimalField, DateTimeField
from django.db.models.fields.related import ForeignKey
from django.conf import settings
from datetime import datetime, timedelta
from time import strftime


class Bid(Model):
    """A bid on an item."""

    amount = DecimalField(max_digits=40, decimal_places=2, verbose_name='Bid Amount')
    user = ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Bidder')
    timestamp = DateTimeField(auto_now_add=True, blank=True, verbose_name='Timestamp')

    def __str__(self):
        return str(self.user) + " - $" + str(self.amount)

    def time_delta(self):
        now = datetime.now()
        elapsed = now - self.timestamp

        if now - timedelta(hours=1) < now - elapsed:
            testdatetime = now - elapsed
            stringtime = testdatetime.strftime("%M")
            return stringtime + " minutes ago"
        elif now - timedelta(hours=2) < now - elapsed:
            return "1 hour ago"
        elif now - timedelta(hours=3) < now - elapsed:
            return "2 hours ago"
        else:
            testdatetime = self.timestamp
            stringtime = testdatetime.strftime("%I:%M %Y-%m-%d ")
            return stringtime
