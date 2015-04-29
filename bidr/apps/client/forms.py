"""
.. module:: bidr.apps.auctions.forms
   :synopsis: Bidr Silent Auction System Auction Forms.

.. moduleauthor:: Jarred Stelfox <>

"""
from django.forms.forms import format

from django.forms.models import ModelForm
from bidr.apps.bids.models import Bid


class ItemBidForm(ModelForm):

    class Meta:
        model = Bid
        fields = ["bid_amount"]