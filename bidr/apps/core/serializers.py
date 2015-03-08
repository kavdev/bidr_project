"""
.. module:: bidr.apps.core.serializers
   :synopsis: Bidr Silent Auction System Core Serializers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import BidrUser
from ..auctions.serializers import GetAuctionModelSerializer


class BidrUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BidrUser
        fields = ('id', 'name', 'email', 'phone_number', 'is_superuser')


class GetBidrUserParticipatedAuctionsSerializer(serializers.ModelSerializer):
    participants = GetAuctionModelSerializer(many=True)

    class Meta:
        model = BidrUser
        fields = ['participants']


class RegisterBidrUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'phone_number', 'password']
