"""
.. module:: bidr.apps.auctions.forms
   :synopsis: Bidr Silent Auction System Auction Forms.

.. moduleauthor:: Jarred Stelfox <>

"""
from django.forms.forms import Form
from django.forms.fields import EmailField

class ManagerForm(Form):
    manager_email = EmailField(validators=[validate_user_exists])