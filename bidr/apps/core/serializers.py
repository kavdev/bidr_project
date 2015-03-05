"""
.. module:: bidr.apps.core.serializers
   :synopsis: Bidr Silent Auction System Core Serializers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model

from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, RelatedField

from .models import BidrUser


class BidrUserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = BidrUser
        fields = ('id', 'name', 'email', 'phone_number', 'is_superuser')


class GetBidrUserParticipatedAuctionsSerializer(ModelSerializer):
    class Meta:
        model = BidrUser
        fields = ['participants']


class RegisterBidrUserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'phone_number', 'password']
