"""
.. module:: bidr.apps.auctions.forms
   :synopsis: Bidr Silent Auction System Auction Forms.

.. moduleauthor:: Jarred Stelfox <>

"""
from django.forms.forms import Form
from django.forms.fields import EmailField
from django.forms.models import ModelForm
from django.core.exceptions import ValidationError


from .validators import validate_user_exists


class ManagerForm(Form):
    manager_email = EmailField(validators=[validate_user_exists])


class AuctionCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AuctionCreateForm, self).__init__(*args, **kwargs)
