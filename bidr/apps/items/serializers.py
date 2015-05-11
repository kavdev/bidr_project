"""
.. module:: bidr.apps.items.serializers
   :synopsis: Bidr Silent Auction System Items Serializers.

.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>

"""

from rest_framework.serializers import ModelSerializer

from .models import AbstractItem
from ..bids.serializers import BidSerializer
from ..core.serializers import BidrUserIDSerializer


class ItemSerializer(ModelSerializer):
    claimed_bid = BidSerializer()
    highest_bid = BidSerializer()
    bidders = BidrUserIDSerializer(many=True)

    class Meta:
        model = AbstractItem
        fields = ['id', 'name', 'description', 'claimed', 'claimed_bid', 'bidders', 'image_urls', 'highest_bid', 'total_starting_bid', 'polymorphic_identifier']
