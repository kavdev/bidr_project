"""
.. module:: bidr.apps.core.serializers
   :synopsis: Bidr Silent Auction System Core Serializers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>

"""

from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

from .models import BidrUser


class RegisterBidrUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'phone_number', 'password']


class BidrUserIDSerializer(ModelSerializer):
    class Meta:
        model = BidrUser
        fields = ['id']
