"""
.. module:: bidr.apps.core.api
   :synopsis: Bidr Silent Auction System Core API Endpoints.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging

from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import BidrUser
from .serializers import RegisterBidrUserSerializer
from ..auctions.serializers import GetBidrUserParticipatedAuctionsSerializer

logger = logging.getLogger(__name__)


class GetBidrUserParticipatedAuctionsView(RetrieveAPIView):
    """
    Use this endpoint to get a list of all the auctions a user has signed up for.
    """
    queryset = BidrUser.objects.all()
    serializer_class = GetBidrUserParticipatedAuctionsSerializer

    permission_classes = (
        IsAuthenticated,
    )


class RegisterBidrUser(APIView):
    permission_classes = ["AllowAny"]

    def post(self, request):
        """Registration code inspired by http://stackoverflow.com/a/19337404."""
        logger.warning(request.data)
        serializer = RegisterBidrUserSerializer(data=request.data)
        valid_fields = [field.name for field in get_user_model()._meta.fields]

        if serializer.is_valid(raise_exception=True):
            user_data = {field: data for (field, data) in request.data.items() if field in valid_fields}
            user = get_user_model().objects.create_user(**user_data)
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=HTTP_400_BAD_REQUEST)
