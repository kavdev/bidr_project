"""
.. module:: bidr.apps.bids.serializers
   :synopsis: Bidr Silent Auction System Bid Serializers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>

"""

from rest_framework.serializers import ModelSerializer, ValidationError, IntegerField

from ..core.templatetags.currency import currency
from ..items.models import AbstractItem
from .models import Bid


class BidSerializer(ModelSerializer):
    class Meta:
        model = Bid
        fields = ['amount', 'user', 'timestamp', 'user_display_name']


class CreateBidSerializer(ModelSerializer):
    item_id = IntegerField(write_only=True, required=True)

    def create(self, validated_data):
        item = AbstractItem.objects.get(id=validated_data['item_id'])
        auction = item.bidables.all()[0]

        if auction.stage > 1:
            raise ValidationError("Auction Over")

        if not item.highest_bid or item.highest_bid.amount < validated_data['amount']:
            if not item.highest_bid or validated_data['amount'] - item.highest_bid.amount >= auction.bid_increment:
                del validated_data['item_id']

                instance = ModelSerializer.create(self, validated_data)
                item.bids.add(instance)
                item.save()

                return instance
            else:
                raise ValidationError([
                    'bid_increment_error',
                    auction.bid_increment,
                    currency(item.highest_bid.amount),
                    item.highest_bid.user.id
                ])
        else:
            raise ValidationError([currency(item.highest_bid.amount), item.highest_bid.user.id])

    class Meta:
        model = Bid
        fields = ['amount', 'user', 'item_id']
