"""
.. module:: bidr.apps.auctions.api
   :synopsis: Bidr Silent Auction System Auction API Endpoints.

.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>

"""

from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from .models import Auction
from .serializers import AddAuctionParticipantSerializer, AuctionSerializer, AuctionItemSerializer


class AddAuctionParticipantView(UpdateAPIView):
    """
    Use this endpoint to add a user to an auction.
    """
    queryset = Auction.objects.all()
    serializer_class = AddAuctionParticipantSerializer

    permission_classes = (
        IsAuthenticated,
    )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Exception as exc:
            return Response(
                data={'detail': 'Not found'},
                status=HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except ValidationError as exc:
            if exc.args[0] == 'This auction requires a password.':
                return Response(
                    data={"password_required": "This auction requires a password."},
                    status=HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    data={"password_incorrect": "The password you entered is incorrect."},
                    status=HTTP_400_BAD_REQUEST,
                )
        return Response(
            data={"participant_added": "The participant was either added or was already signed up for the auction.",
                  "name": instance.name,
                  "id": instance.id,
                  "stage": instance.stage},
            status=HTTP_200_OK,
        )


class RetrieveAuctionAPIView(RetrieveAPIView):
    """
    Use this endpoint to get an auction model.
    """
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

    permission_classes = (
        IsAuthenticated,
    )


class RetrieveAuctionItemView(RetrieveAPIView):
    """
    Use this endpoint to get an auction model.
    """
    queryset = Auction.objects.all()
    serializer_class = AuctionItemSerializer

    permission_classes = (
        IsAuthenticated,
    )
