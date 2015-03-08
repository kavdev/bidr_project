"""
.. module:: bidr.apps.bids.serializers
   :synopsis: Bidr Silent Auction System Bid Serializers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.db.models import Max

from rest_framework.serializers import HyperlinkedModelSerializer, ValidationError, ModelSerializer, IntegerField

from .models import Bid
from ..items.models import AbstractItem


class BidSerializer(HyperlinkedModelSerializer):

    def validate_amount(self, value):
        """Check that the blog post is about Django."""

        agg = Bid.objects.aggregate(Max('amount'))["amount__max"]

        if agg and value < agg:
            raise ValidationError("Your bid must exceed the current bid amount.")
        return value

    class Meta:
        model = Bid
        fields = ('amount', 'user')


class GetBidModelSerializer(ModelSerializer):
    class Meta:
        model = Bid
        fields = ['amount', 'user', 'timestamp']


class CreateBidSerializer(ModelSerializer):
    itemID = IntegerField(write_only=True, required=True)

    def create(self, validated_data):
        item = AbstractItem.objects.get(id=validated_data['itemID'])
        if item.highest_bid.amount < validated_data['amount']:
            del validated_data['itemID']
            instance = ModelSerializer.create(self, validated_data)
            item.bids.add(instance)
            item.save()
            return instance
        else:
            raise ValidationError(item.highest_bid.amount)

    class Meta:
        model = Bid
        fields = ['amount', 'user', 'itemID']
