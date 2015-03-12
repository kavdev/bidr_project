"""
.. module:: bidr.apps.bids.serializers
   :synopsis: Bidr Silent Auction System Bid Serializers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from rest_framework.serializers import ModelSerializer, ValidationError, IntegerField

from .models import Bid
from ..core.templatetags.currency import currency
from ..items.models import AbstractItem


class BidSerializer(ModelSerializer):
    class Meta:
        model = Bid
        fields = ['amount', 'user', 'timestamp']


class CreateBidSerializer(ModelSerializer):
    item_id = IntegerField(write_only=True, required=True)

    def create(self, validated_data):
        item = AbstractItem.objects.get(id=validated_data['item_id'])

        if not item.highest_bid or item.highest_bid.amount < validated_data['amount']:
            del validated_data['item_id']

            instance = ModelSerializer.create(self, validated_data)
            item.bids.add(instance)
            item.save()

            return instance
        else:
            raise ValidationError(currency(item.highest_bid.amount))

    class Meta:
        model = Bid
        fields = ['amount', 'user', 'item_id']
