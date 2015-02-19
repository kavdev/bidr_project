"""
.. module:: bidr.apps.items.views
   :synopsis: Bidr Silent Auction System Item Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import redirect

from ..auctions.models import Auction
from ..items.models import Item


class ItemCreateView(CreateView):
    template_name = "items/create_item.html"
    model = Item
    fields = ["name", "description", "min_price", "picture"]
    success_url = reverse_lazy("create_item")

    def form_valid(self, form):
        self.object = form.save()
        auction_instance = Auction.objects.get(id=self.kwargs['auction_id'])
        auction_instance.bidables.add(self.object)
        auction_instance.save()
        return redirect(self.get_success_url())
