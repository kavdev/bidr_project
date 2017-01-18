"""
.. module:: bidr.apps.bids.models
   :synopsis: Bidr Silent Auction System Bid Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from datetime import timedelta
import math

from django.conf import settings
from django.db.models.base import Model
from django.db.models.fields import DateTimeField, BigIntegerField
from django.db.models.fields.related import ForeignKey
from django.template.defaultfilters import pluralize
from django.utils.timezone import now


class Bid(Model):
    """A bid on an item."""

    amount = BigIntegerField(verbose_name='Bid Amount')
    user = ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Bidder')
    timestamp = DateTimeField(auto_now_add=True, blank=True, verbose_name='Timestamp')

    @property
    def user_display_name(self):
        return self.user.display_name

    def __str__(self):
        return str(self.user) + " - $" + str(self.amount)

    def time_delta(self):
        current_time = now()
        elapsed = current_time - self.timestamp

        if current_time - timedelta(hours=1) < current_time - elapsed:
            minutes_ago = math.ceil(elapsed.seconds / 60)
            return str(minutes_ago) + " minute" + pluralize(minutes_ago) + " ago"
        elif current_time - timedelta(hours=2) < current_time - elapsed:
            return "1 hour ago"
        elif current_time - timedelta(hours=3) < current_time - elapsed:
            return "2 hours ago"
        elif current_time - timedelta(hours=4) < current_time - elapsed:
            return "3 hours ago"
        else:
            return self.timestamp.strftime("%Y-%m-%d  %H:%M")
