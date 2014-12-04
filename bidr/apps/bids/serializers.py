"""
.. module:: bidr.apps.bids.serializers
   :synopsis: Bidr Silent Auction System Bid Serializers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Bid


class BidSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Bid
        fields = ('amount', 'user')
