"""
.. module:: bidr.apps.items.forms
   :synopsis: Bidr Silent Auction System Item Forms.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

from django.forms.models import ModelForm

from .models import Item


class ItemCreateForm(ModelForm):

    class Meta:
        model = Item
        fields = ["name", "description", "minimum_price", "picture"]
