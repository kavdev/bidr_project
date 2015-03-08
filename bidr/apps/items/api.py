from rest_framework import generics, permissions

from .models import AbstractItem
from .serializers import GetItemModelSerializer


class GetItemModelView(generics.RetrieveAPIView):
    """
    Use this endpoint to get a list of all the auctions a user has signed up for.
    """
    queryset = AbstractItem.objects.all()
    serializer_class = GetItemModelSerializer

    permission_classes = (
        permissions.IsAuthenticated,
    )
