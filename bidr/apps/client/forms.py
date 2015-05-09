"""
.. module:: bidr.apps.client.forms
   :synopsis: Bidr Silent Auction System Forms.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Jarred Stelfox

"""

import datetime

from django.core.exceptions import ValidationError
from django.forms.fields import IntegerField
from django.forms.models import ModelForm

from ..auctions.models import Auction, STAGES
from ..auctions.utils import _end_auction
from ..bids.models import Bid
from ..core.templatetags.currency import currency


class AddAuctionForm(ModelForm):
    auction_id = IntegerField(min_value=0, required=True)

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

    class Meta:
        model = Auction
        fields = ["auction_id", "optional_password"]


class AddBidForm(ModelForm):

    def __init__(self, item_instance, auction_instance, *args, **kwargs):
        super(AddBidForm, self).__init__(*args, **kwargs)
        self.auction_instance = auction_instance
        self.item_instance = item_instance

    def clean(self):
        if datetime.datetime.now() > self.auction_instance.end_time or self.auction_instance.stage > STAGES.index("Observe"):
            # End the auction if it hasn't ended already
            _end_auction(self.auction_instance)

            raise ValidationError("The auction has already ended. Unable to place bid.")

    def clean_amount(self):
        # Check if the bid is greater than or equal to the starting bid
        if self.cleaned_data['amount'] < self.item_instance.starting_bid + self.auction_instance.bid_increment:
            raise ValidationError("New bid must not be less than " + str(currency(self.item_instance.starting_bid + self.auction_instance.bid_increment)))

        # Check if the bid is greater than or equal to the current highest bid
        if self.item_instance.highest_bid and self.cleaned_data['amount'] < self.item_instance.highest_bid.amount + self.auction_instance.bid_increment:
            raise ValidationError("New bid must not be less than " + str(currency(self.item_instance.highest_bid.amount + self.auction_instance.bid_increment)))

        return self.cleaned_data['amount']

    class Meta:
        model = Bid
        fields = ["amount"]
