"""
.. module:: bidr.apps.items.api
   :synopsis: Bidr Silent Auction System Item API Endpoints.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import AbstractItem
from .serializers import ItemSerializer


class RetrieveItemAPIView(RetrieveAPIView):
    """
    Use this endpoint to get a list of all the auctions a user has signed up for.
    """
    queryset = AbstractItem.objects.all()
    serializer_class = ItemSerializer

    permission_classes = (
        IsAuthenticated,
    )
