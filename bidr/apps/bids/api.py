"""
.. module:: bidr.apps.bids.api
   :synopsis: Bidr Silent Auction System Bid API Endpoints.

.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>

"""

from django.template.loader import render_to_string

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
            if exc.detail[0] == "Auction Over":
                return Response(
                    data={"auction_over": exc.detail[0],
                        "exception_message": "This auction has ended."},
                    status=HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    data={"current_highest_bid": exc.detail[0],
                        "exception_message": "Your bid must be greater than the current highest bid of " + exc.detail[0]},
                    status=HTTP_400_BAD_REQUEST,
                )
        headers = self.get_success_headers(serializer.data)

        bid_item_queryset = instance.bids
        bid_item = bid_item_queryset.all()[0]
        outbid_bid = bid_item.get_second_highest_bid()
#        auction = bid_item.bidables.all()[0]

        if outbid_bid and outbid_bid.user.email != instance.user.email:
            kwargs = {"item": bid_item, "absolute_client_url": bid_item.get_absolute_client_url(self.request), "bid": instance.amount, "outbidder": instance.user}
            text_content = render_to_string("email/outbid_notification.txt", kwargs)
            html_content = render_to_string("email/outbid_notification.html", kwargs)

            outbid_bid.user.email_user(subject="Bidr: You've been outbid!",
                                       message=text_content, html_message=html_content)
#             if outbid_bid.user.ios_device_token is not None:
#                 payload = Payload(alert="Outbid", sound="default", badge=1)
#                 auction.apns.gateway_server.send_notification(outbid_bid.user.ios_device_token, payload)

        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
