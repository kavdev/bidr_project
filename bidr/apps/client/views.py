"""
.. module:: bidr.apps.client.views
   :synopsis: Bidr Silent Auction System Client Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from ..items.models import AbstractItem
from ..auctions.models import Auction, STAGES
from ..core.views import LoginView as AdminLoginView
from .forms import AddAuctionForm


class LoginView(AdminLoginView):
    template_name = "client/login.html"
    success_url = reverse_lazy("client:home")


class AuctionListView(TemplateView):
    template_name = "client/auction_list.html"
    model = Auction

    def get_queryset(self):
        return self.request.user.participants

    def get_context_data(self, **kwargs):
        context = super(AuctionListView, self).get_context_data(**kwargs)
        context["upcoming_auctions"] = self.get_queryset().filter(stage=STAGES.index("Plan"))
        context["current_auctions"] = self.get_queryset().filter(stage=STAGES.index("Observe"))
        context["complete_auctions"] = self.get_queryset().filter(stage__gte=STAGES.index("Claim"))
        return context


class ItemListView(TemplateView):
    template_name = "client/auction_items.html"

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        auction_instance = Auction.objects.get(id=kwargs["auction_id"])
        context["auction_name"] = auction_instance.name
        context["my_bids"] = auction_instance.get_my_bids(self.request.user)
        context["other_items"] = auction_instance.get_other_items(self.request.user)
        return context


class ItemDetailView(DetailView):
    template_name = "client/item_details.html"
    model = AbstractItem

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        return context


class AddAuctionView(FormView):
    template_name = "client/add_auction.html"
    form_class = AddAuctionForm
    # TODO: Change to the auction's item list view
    success_url = reverse_lazy("client:home")

    def form_valid(self, form):
        auction_instance = Auction.objects.get(id=form.cleaned_data["auction_id"])
        auction_instance.participants.add(self.request.user)
        auction_instance.save()
        return super(AddAuctionView, self).form_valid(form)
