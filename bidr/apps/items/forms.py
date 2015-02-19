"""
.. module:: bidr.apps.items.forms
   :synopsis: Bidr Silent Auction System Item Forms.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.forms.models import ModelForm

from .models import Item


class ItemCreateForm(ModelForm):

    class Meta:
        model = Item
        fields = ["name", "description", "min_price", "picture"]
