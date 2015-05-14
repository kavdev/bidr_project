"""
.. module:: bidr.apps.bids.models
   :synopsis: Bidr Silent Auction System Bid Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from datetime import datetime, timedelta
import math

from django.db.models.base import Model
from django.db.models.fields import DateTimeField, IntegerField
from django.db.models.fields.related import ForeignKey
from django.conf import settings
from django.template.defaultfilters import pluralize


class Bid(Model):
    """A bid on an item."""

    amount = IntegerField(verbose_name='Bid Amount')
    user = ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Bidder')
    timestamp = DateTimeField(auto_now_add=True, blank=True, verbose_name='Timestamp')

    def __str__(self):
        return str(self.user) + " - $" + str(self.amount)

    def time_delta(self):
        now = datetime.now()
        elapsed = now - self.timestamp

        if now - timedelta(hours=1) < now - elapsed:
            minutes_ago = math.ceil(elapsed.seconds / 60)
            return str(minutes_ago) + " minute" + pluralize(minutes_ago) + " ago"
        elif now - timedelta(hours=2) < now - elapsed:
            return "1 hour ago"
        elif now - timedelta(hours=3) < now - elapsed:
            return "2 hours ago"
        elif now - timedelta(hours=4) < now - elapsed:
            return "3 hours ago"
        elif (now - timedelta(hours=4) > now - elapsed and
              datetime.today().year == self.timestamp.year and
              datetime.today().month == self.timestamp.month and
              datetime.today().day == self.timestamp.day):
            return self.timestamp.strftime("%H:%M")
        else:
            return self.timestamp.strftime("%Y-%m-%d  %H:%M")
