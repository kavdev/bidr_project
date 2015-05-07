"""
.. module:: bidr.apps.bids.api
   :synopsis: Bidr Silent Auction System Bid API Endpoints.

.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>

"""

from django.core.mail import send_mail

from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.serializers import ValidationError

from .models import Bid
from .serializers import BidSerializer, CreateBidSerializer


class RetrieveBidAPIView(RetrieveAPIView):
    """
    Use this endpoint to get a bid.
    """
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    permission_classes = (
        IsAuthenticated,
    )


class CreateBidAPIView(CreateAPIView):
    """
    Use this endpoint to create a bid.
    """
    serializer_class = CreateBidSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            instance = self.perform_create(serializer)
        except ValidationError as exc:
            return Response(
                data={"current_highest_bid": exc.detail[0],
                      "exception_message": "Your bid must be greater than the current highest bid of " + exc.detail[0]},
                status=HTTP_400_BAD_REQUEST,
            )
        headers = self.get_success_headers(serializer.data)

        emails = []
        bid_item_queryset = instance.bids
        bid_item = bid_item_queryset.all()[0]
        outbid_bid = bid_item.get_second_highest_bid()

        if outbid_bid and outbid_bid.user.email != instance.user.email:
            emails.append(outbid_bid.user.email)

            send_mail(subject="Bidr: You've been outbid!",
                message="Oh No! You've been outbid on the item '{item}' with a bid of ${bid}".format(item=bid_item.name, bid=instance.amount),
                from_email="Bidr Mail Relay Server <do-not-reply@bidr.herokuapp.com",
                recipient_list=emails)

        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
