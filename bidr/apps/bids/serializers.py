"""
.. module:: bidr.apps.bids.serializers
   :synopsis: Bidr Silent Auction System Bid Serializers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.db.models import Max

from rest_framework.serializers import HyperlinkedModelSerializer, ValidationError, ModelSerializer

from .models import Bid


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
