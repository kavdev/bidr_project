"""
.. module:: bidr.apps.Admin.views
   :synopsis: Bidr Silent Auction Admin Views.

.. moduleauthor:: Jarred Stelfox <sstelfox@calpoly.edu>
"""

from django.views.generic import ListView
from .models import Auction


class AuctionView(ListView):
    template_name = "auctions/auctions.html"

    def get_queryset(self):
        return Auction.objects.all()
