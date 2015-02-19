"""
.. module:: bidr.apps.items.models
   :synopsis: Bidr Silent Auction System Item Models.

.. moduleauthor:: Jarred Stelfox <sstelfox@calpoly.edu>

"""

from django.views.generic.detail import DetailView

from .models import AbstractItem
from rest_framework.urls import template_name


class ItemDetailView(DetailView):
    template_name = "auctions/itemdetail.html"
    model = AbstractItem
    
    def get_object(self, queryset=None):
        return AbstractItem.objects.get(bidables__id=self.kwargs['auction_id'], bidables__auctions__slug=self.kwargs['slug'], id=self.kwargs['item_id'])