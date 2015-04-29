"""
.. module:: bidr.apps.client.views
   :synopsis: Bidr Silent Auction System Client Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from ..auctions.models import Auction, STAGES
from ..bids.models import Bid
from ..core.views import LoginView as AdminLoginView
from ..items.models import AbstractItem
from .forms import AddAuctionForm, AddBidForm


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
    template_name = "client/auction_item_list.html"

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        auction_instance = Auction.objects.get(id=self.kwargs["auction_id"])
        context["auction"] = auction_instance
        context["my_bids"] = auction_instance.get_my_bids(self.request.user)
        context["other_items"] = auction_instance.get_other_items(self.request.user)
        return context


class ItemDetailView(FormView):
    template_name = "client/auction_item_detail.html"
    form_class = AddBidForm

    item_instance = None
    auction_instance = None

    def get_objects(self):
        if not self.item_instance:
            self.item_instance = AbstractItem.objects.get(id=self.kwargs["pk"])

        if not self.auction_instance:
            self.auction_instance = Auction.objects.get(id=self.kwargs["auction_id"])

        return self.auction_instance, self.item_instance

    def form_valid(self, form):
        bid_instance = Bid.objects.create(user=self.request.user, amount=form.cleaned_data['amount'])
        auction_instance, item_instance = self.get_objects()

        item_instance.bids.add(bid_instance)
        item_instance.save()

        return super(FormView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        auction_instance, item_instance = self.get_objects()
        kwargs["item_instance"] = item_instance
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        auction_instance, item_instance = self.get_objects()
        context["object"] = item_instance
        context["auction"] = auction_instance
        return context

    def get_success_url(self):
        auction_instance, item_instance = self.get_objects()
        return reverse("item_list", kwargs={"auction_id": auction_instance.id})


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
