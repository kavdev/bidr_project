"""
.. module:: bidr.apps.client.views
   :synopsis: Bidr Silent Auction System Client Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>

"""

from django.core.urlresolvers import reverse_lazy, reverse
from django.template.loader import render_to_string
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
    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        auction_instance = Auction.objects.get(id=self.kwargs["auction_id"])
        context["auction"] = auction_instance
        context["my_bids"] = auction_instance.get_items_user_has_bid_on(self.request.user)
        context["winning_items"] = auction_instance.get_items_user_is_winning(self.request.user)
        context["losing_items"] = auction_instance.get_items_user_is_losing(self.request.user)
        context["other_items"] = auction_instance.get_items_user_has_not_bid_on(self.request.user)
        context["all_items"] = list(auction_instance.bidables.all())
        return context

    def get_template_names(self):
        auction_instance = Auction.objects.get(id=self.kwargs["auction_id"])
        if auction_instance.stage == 0:
            return ["client/auction_upcoming_item_list.html"]
        elif auction_instance.stage == 1:
            return ["client/auction_current_item_list.html"]
        else:
            return ["client/auction_complete_item_list.html"]


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

        outbid_bid = item_instance.get_second_highest_bid()

        if outbid_bid and outbid_bid.user.email != self.request.user.email:
            kwargs = {"item": item_instance, "absolute_client_url": item_instance.get_absolute_client_url(self.request), "bid": bid_instance.amount, "outbidder": bid_instance.user}
            text_content = render_to_string("email/outbid_notification.txt", kwargs)
            html_content = render_to_string("email/outbid_notification.html", kwargs)

            outbid_bid.user.email_user(subject="Bidr: You've been outbid!",
                                       message=text_content, html_message=html_content)

        return super(FormView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        auction_instance, item_instance = self.get_objects()
        kwargs["item_instance"] = item_instance
        kwargs["auction_instance"] = auction_instance
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        auction_instance, item_instance = self.get_objects()
        context["object"] = item_instance
        context["auction"] = auction_instance
        context["bid_on_item"] = item_instance in auction_instance.get_items_user_has_bid_on(self.request.user)
        if item_instance.highest_bid is not None:
            context["winning_item"] = item_instance.highest_bid.user == self.request.user
        else:
            context["winning_item"] = False
        context["previous_bid"] = item_instance.get_previous_bid_by_user(self.request.user)
        return context

    def get_success_url(self):
        auction_instance, item_instance = self.get_objects()
        return reverse("client:item_list", kwargs={"auction_id": auction_instance.id})


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
