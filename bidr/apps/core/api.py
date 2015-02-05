"""
.. module:: bidr.apps.core.api
   :synopsis: Bidr Silent Auction System Core API Endpoints.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import BidrUser
from .serializers import BidrUserSerializer, RegisterBidrUserSerializer

logger = logging.getLogger(__name__)


class BidrUserViewSet(ModelViewSet):
    """API endpoint that allows bids to be viewed or edited."""

    queryset = BidrUser.objects.all()
    serializer_class = BidrUserSerializer


class RegisterBidrUser(APIView):

    def post(self, request):
        """Registration code inspired by http://stackoverflow.com/a/19337404."""
        logger.info(request.data)
        serializer = RegisterBidrUserSerializer(data=request.data)
        logger.infor("here1")
        valid_fields = [field.name for field in get_user_model()._meta.fields]
        logger.infor("here2")

        if serializer.is_valid(raise_exception=True):
            logger.infor("here3")
            user_data = {field: data for (field, data) in request.data.items() if field in valid_fields}
            logger.infor("here4")
            user = get_user_model().objects.create_user(**user_data)
            logger.infor("here5")
            token = Token.objects.create(user=user)
            logger.infor("here6")
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
