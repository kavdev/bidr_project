"""
.. module:: bidr.apps.core.api
   :synopsis: Bidr Silent Auction System Core API Endpoints.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import BidrUser
from .serializers import BidrUserSerializer, RegisterBidrUserSerializer


class BidrUserViewSet(ModelViewSet):
    """API endpoint that allows bids to be viewed or edited."""

    queryset = BidrUser.objects.all()
    serializer_class = BidrUserSerializer


@api_view(['POST'])
def register_bidr_user(request):
    VALID_USER_FIELDS = [f.name for f in get_user_model()._meta.fields]

    serialized = RegisterBidrUserSerializer(data=request.DATA)
    if serialized.is_valid():
        user_data = {field: data for (field, data) in request.DATA.items() if field in VALID_USER_FIELDS}
        user = get_user_model().objects.create_user(**user_data)
        return Response(RegisterBidrUserSerializer(instance=user).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
