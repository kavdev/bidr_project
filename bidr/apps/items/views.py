"""
.. module:: bidr.apps.items.views
   :synopsis: Bidr Silent Auction System Item Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect

from ..auctions.models import Auction
from ..items.models import Item, ItemCollection


class ItemCreateView(CreateView):
    template_name = "items/create_item.html"
    model = Item
    fields = ["name", "description", "minimum_price", "picture"]

    def form_valid(self, form):
        self.object = form.save()
        auction_instance = Auction.objects.get(id=self.kwargs['auction_id'])
        auction_instance.bidables.add(self.object)
        auction_instance.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('create_item', kwargs={'slug': self.kwargs['slug'], 'auction_id': self.kwargs['auction_id']})


class ItemUpdateView(UpdateView):
    template_name = "items/update_item.html"
    model = Item
    fields = ['name', 'description', 'minimum_price', 'picture']

    def get_success_url(self):
        return reverse_lazy('update_item', kwargs={'slug': self.kwargs['slug'], 'auction_id': self.kwargs['auction_id'], 'pk': self.object.id})


class ItemCollectionCreateView(CreateView):
    template_name = "items/create_item_collection.html"
    model = ItemCollection
    fields = ["name", "description"]

    def form_valid(self, form):
        self.object = form.save()
        auction_instance = Auction.objects.get(id=self.kwargs['auction_id'])
        auction_instance.bidables.add(self.object)
        auction_instance.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('create_item_collection', kwargs={'slug': self.kwargs['slug'], 'auction_id': self.kwargs['auction_id']})


class ItemCollectionUpdateView(UpdateView):
    template_name = "items/update_item_collection.html"
    model = ItemCollection
    fields = ['name', 'description']

    def get_success_url(self):
        return reverse_lazy('update_item_collection', kwargs={'slug': self.kwargs['slug'], 'auction_id': self.kwargs['auction_id'], 'pk': self.object.id})
