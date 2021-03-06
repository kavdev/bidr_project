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
        fields = ['name', 'display_name', 'email', 'phone_number', 'password']


class BidrUserIDSerializer(ModelSerializer):
    class Meta:
        model = BidrUser
        fields = ['id']


class UpdateBidrUserIOSDeviceTokenSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        ios_device_token = validated_data.get('ios_device_token')
        # "(null)" is what the iphone simulator sends over the api for some reason
        if ios_device_token and ios_device_token != ('(null)'):
            instance.ios_device_token = validated_data.get('ios_device_token')
            instance.save()
        return instance

    class Meta:
        model = get_user_model()
        fields = ['ios_device_token']
