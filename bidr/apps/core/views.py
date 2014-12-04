"""
.. module:: bidr.apps.core.views
   :synopsis: Bidr Silent Auction System Core Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from rest_framework.viewsets import ModelViewSet

from .models import Bidder
from .serializers import BidderSerializer


class BidderViewSet(ModelViewSet):
    """API endpoint that allows bids to be viewed or edited."""

    queryset = Bidder.objects.all()
    serializer_class = BidderSerializer
