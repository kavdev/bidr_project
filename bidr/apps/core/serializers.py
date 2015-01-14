"""
.. module:: bidr.apps.core.serializers
   :synopsis: Bidr Silent Auction System Core Serializers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from rest_framework.serializers import HyperlinkedModelSerializer

from .models import BidrUser


class BidrUserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = BidrUser
        fields = ('id', 'name', 'email', 'phone_number', 'is_superuser')
