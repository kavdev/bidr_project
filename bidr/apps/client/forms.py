"""
.. module:: bidr.apps.client.forms
   :synopsis: Bidr Silent Auction System Forms.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Jarred Stelfox

"""

from django.core.exceptions import ValidationError
from django.forms.fields import IntegerField
from django.forms.models import ModelForm

from ..auctions.models import Auction
from ..bids.models import Bid
from ..core.templatetags.currency import currency


class AddAuctionForm(ModelForm):
    auction_id = IntegerField(min_value=0, required=True)

    class Meta:
        model = Auction
        fields = ["auction_id", "optional_password"]

    def clean(self):
        try:
            auction_instance = Auction.objects.get(id=self.cleaned_data["auction_id"])
        except Auction.DoesNotExist:
            raise ValidationError('An auction with this ID does not exist.')

        if auction_instance.optional_password and (auction_instance.optional_password != self.cleaned_data.get('optional_password')):
            if not self.cleaned_data.get('optional_password'):
                message = 'This auction requires an auction password.'
            else:
                message = 'The password you entered is incorrect.'

            raise ValidationError(message)

        return self.cleaned_data


class AddBidForm(ModelForm):

    def __init__(self, item_instance, *args, **kwargs):
        super(AddBidForm, self).__init__(*args, **kwargs)
        self.item_instance = item_instance

    def clean_amount(self):
        if self.item_instance.highest_bid and self.cleaned_data['amount'] <= self.item_instance.highest_bid.amount:
            raise ValidationError("New bid must be greater than " + str(currency(self.item_instance.highest_bid.amount)))
        else:
            return self.cleaned_data['amount']

    class Meta:
        model = Bid
        fields = ["amount"]
