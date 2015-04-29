"""
.. module:: bidr.apps.client.views
   :synopsis: Bidr Silent Auction System Client Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from ..items.models import AbstractItem
from ..auctions.models import Auction, STAGES
from ..core.views import LoginView as AdminLoginView


class LoginView(AdminLoginView):
    template_name = "client/login.html"
    success_url = reverse_lazy("client:home")


class AuctionListView(TemplateView):
    template_name = "client/auction_list.html"
    model = Auction

    def get_queryset(self):
        return self.request.user.participants


class ItemListView(TemplateView):
    template_name = "client/auction_items.html"

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        auction_instance = Auction.objects.get(id=kwargs["auction_id"])
        context["auction_name"] = auction_instance.name
        context["my_bids"] = auction_instance.get_my_bids(self.request.user)
        context["other_items"] = auction_instance.get_other_items(self.request.user)
        return context


class ItemDetailView(FormView):
    template_name = "client/item_details.html"
    model = AbstractItem

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context["upcoming_auctions"] = self.get_queryset().filter(stage=STAGES.index("Plan"))
        context["current_auctions"] = self.get_queryset().filter(stage=STAGES.index("Observe"))
        context["complete_auctions"] = self.get_queryset().filter(stage__gte=STAGES.index("Claim"))
        return context
