from django.contrib.auth import get_user_model
from bidr.apps.auctions.models import Auction

from rest_framework.serializers import HyperlinkedModelSerializer, EmailField, ValidationError

from ..items.serializers import ItemSerializer


class AddAuctionParticipantSerializer(HyperlinkedModelSerializer):
    user_email = EmailField(write_only=True, required=True, allow_blank=False)

    def update(self, instance, validated_data):
        user = get_user_model().objects.get(email=validated_data['user_email'])

        if instance.optional_password:
            if instance.optional_password == validated_data.get('optional_password'):
                instance.participants.add(user)
                instance.save()
            else:
                if not validated_data.get('optional_password'):
                    message = 'This auction requires a password.'
                else:
                    message = 'The password you entered is incorrect.'

                raise ValidationError(message)
        else:
            instance.participants.add(user)
            instance.save()
        return instance

    class Meta:
        model = Auction
        fields = ['optional_password', 'user_email']


class AuctionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Auction
        fields = ['name', 'stage', 'id']


class AuctionItemSerializer(HyperlinkedModelSerializer):
    bidables = ItemSerializer(many=True)

    class Meta:
        model = Auction
        fields = ['bidables']
