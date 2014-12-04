"""
.. module:: bidr.apps.bids.views
   :synopsis: Bidr Silent Auction System Bid Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.mail import send_mail
from django.db.models import Max

from django_ajax.decorators import ajax
from rest_framework.viewsets import ModelViewSet

from ..core.models import Bidder
from .models import Bid
from .serializers import BidSerializer


class BidViewSet(ModelViewSet):
    """API endpoint that allows bids to be viewed or edited."""

    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        emails = []
        for bidder in Bidder.objects.exclude(id=instance.user.id):
            emails.append(bidder.email)

        send_mail(subject="Bidr: You've been outbid!",
                  message="Oh No! You've been outbid by {user} with a bid of {bid}".format(user=instance.user, bid=instance.amount),
                  from_email="Bidr Mail Relay Server <do-not-reply@bidr.herokuapp.com",
                  recipient_list=emails)


@ajax
def get_max_bid(request):
    return {'max_bid': Bid.objects.aggregate(Max('amount'))["amount__max"]}
