"""
.. module:: bidr.apps.Admin.views
   :synopsis: Bidr Silent Auction Admin Views.

.. moduleauthor:: Jarred Stelfox <sstelfox@calpoly.edu>
"""

from django.views.generic import ListView
from django.views.generic import CreateView

from .models import Auction


class AuctionView(ListView):
    template_name = "auctions/auctions.html"

    def get_queryset(self):
        return Auction.objects.all()


class AuctionCreateView(CreateView):
    template_name = "auctions/create.html"
    model = Auction
    fields = ['name', 'description', 'start_time', 'end_time', 'optional_password']
