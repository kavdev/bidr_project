"""
.. module:: bidr.apps.bids.views
   :synopsis: Bidr Silent Auction System Bid Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from rest_framework.viewsets import ModelViewSet

from ..core.models import Bidder
from .models import Bid
from .serializers import BidSerializer


class BidViewSet(ModelViewSet):
    """API endpoint that allows bids to be viewed or edited."""

    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def perform_update(self, serializer):
        for bidder in Bidder.objects.exclude(id=self.request.user.id):
            bidder.email_user(subject="Bidr: You've been outbid!",
                              message="Oh No! You've been outbid!",
                              from_email="Bidr Mail Relay Server <do-not-reply@bidr.herokuapp.com")

        super(BidViewSet, self).perform_update(serializer)
