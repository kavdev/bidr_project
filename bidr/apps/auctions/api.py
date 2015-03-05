from rest_framework import generics, permissions, serializers, response, status

from .serializers import AddAuctionParticipantSerializer
from .models import Auction


class AddAuctionParticipantView(generics.UpdateAPIView):
    """
    Use this endpoint to add a user to an auction.
    """
    queryset = Auction.objects.all()
    serializer_class = AddAuctionParticipantSerializer

    permission_classes = (
        permissions.IsAuthenticated,
    )

    # override update to change Response
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except serializers.ValidationError as exc:
            if exc.args[0] == 'This auction requires a password.':
                return response.Response(
                    data={"password_required": "This auction requires a password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return response.Response(
                    data={"password_incorrect": "The password you entered is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return response.Response(
            data={"participant_added": "The participant was either added or was already signed up for the auction."},
            status=status.HTTP_200_OK,
        )
