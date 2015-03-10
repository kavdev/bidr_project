from rest_framework.serializers import ModelSerializer

from .models import AbstractItem
from ..bids.serializers import BidSerializer


class ItemSerializer(ModelSerializer):
    claimed_bid = BidSerializer()
    highest_bid = BidSerializer()
    bids = BidSerializer(many=True)

    class Meta:
        model = AbstractItem
        fields = ['id', 'name', 'description', 'claimed', 'claimed_bid', 'bids', 'image_url', 'highest_bid', 'min_price']
