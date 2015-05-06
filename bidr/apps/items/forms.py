"""
.. module:: bidr.apps.items.forms
   :synopsis: Bidr Silent Auction System Item Forms.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
# from django.forms.fields import DecimalField


from .models import Item
from .validator import validate_minimum_price


class ItemCreateForm(ModelForm):

    class Meta:
        model = Item
        fields = ["name", "description", "minimum_price", "picture"]
