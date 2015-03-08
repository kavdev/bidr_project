from rest_framework import serializers

from .models import AbstractItem
from ..bids.serializers import GetBidModelSerializer


class GetItemModelSerializer(serializers.ModelSerializer):
    claimed_bid = GetBidModelSerializer()
    highest_bid = GetBidModelSerializer()

    class Meta:
        model = AbstractItem
        fields = ['id', 'name', 'description', 'claimed', 'claimed_bid', 'bids', 'image_url', 'highest_bid', 'min_price']
