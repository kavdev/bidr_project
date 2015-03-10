"""
.. module:: bidr.apps.core.serializers
   :synopsis: Bidr Silent Auction System Core Serializers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

from .models import BidrUser
from ..auctions.serializers import AuctionSerializer


class GetBidrUserParticipatedAuctionsSerializer(ModelSerializer):
    participants = AuctionSerializer(many=True)

    class Meta:
        model = BidrUser
        fields = ['participants']


class RegisterBidrUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'phone_number', 'password']
