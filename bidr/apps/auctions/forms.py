"""
.. module:: bidr.apps.auctions.forms
   :synopsis: Bidr Silent Auction System Auction Forms.

.. moduleauthor:: Jarred Stelfox <>

"""

from django.core.exceptions import ValidationError
from django.forms.forms import Form
from django.forms.fields import EmailField
from django.forms.models import ModelForm

from .validators import validate_user_exists
from .models import Auction


class ManagerForm(Form):
    manager_email = EmailField(validators=[validate_user_exists])


class AuctionCreateForm(ModelForm):

    def clean(self):
        if self.cleaned_data["end_time"] <= self.cleaned_data["start_time"]:
            raise ValidationError("The auction's start time must be before its end time.")

        return self.cleaned_data

    class Meta:
        model = Auction
        fields = ["name", "description", "start_time", "end_time", "bid_increment", "optional_password"]
