"""
.. module:: bidr.apps.core.serializers
   :synopsis: Bidr Silent Auction System Core Serializers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Bidder


class BidderSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Bidder
        fields = ('name', 'email', 'phone_number', 'is_superuser')
