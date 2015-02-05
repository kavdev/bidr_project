"""
.. module:: bidr.apps.core.api
   :synopsis: Bidr Silent Auction System Core API Endpoints.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import BidrUser
from .serializers import BidrUserSerializer, RegisterBidrUserSerializer


class BidrUserViewSet(ModelViewSet):
    """API endpoint that allows bids to be viewed or edited."""

    queryset = BidrUser.objects.all()
    serializer_class = BidrUserSerializer


class RegisterBidrUser(APIView):

    def post(self, request):
        """Registration code inspired by http://stackoverflow.com/a/19337404."""
        print(request.data)
        serializer = RegisterBidrUserSerializer(data=request.data)
        valid_fields = [field.name for field in get_user_model()._meta.fields]

        if serializer.is_valid(raise_exception=True):
            user_data = {field: data for (field, data) in request.data.items() if field in valid_fields}
            user = get_user_model().objects.create_user(**user_data)
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
