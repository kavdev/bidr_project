"""
.. module:: bidr.apps.bids.views
   :synopsis: Bidr Silent Auction System Bid Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from rest_framework.viewsets import ModelViewSet

from .models import Bid
from .serializers import BidSerializer


class BidViewSet(ModelViewSet):
    """API endpoint that allows bids to be viewed or edited."""

    queryset = Bid.objects.all()
    serializer_class = BidSerializer
