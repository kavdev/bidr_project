"""
.. module:: bidr.apps.auctions.views
   :synopsis: Bidr Silent Auction System Auction Views.

.. moduleauthor:: Jarred Stelfox <sstelfox@calpoly.edu>
.. moduleauthor:: Alexander Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

from ..organizations.models import Organization
from .models import Auction


class AuctionView(ListView):
    template_name = "auctions/auctions.html"

    def get_queryset(self):
        return Auction.objects.managed_by(self.request.user).filter(auctions__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(AuctionView, self).get_context_data(**kwargs)
        context["org_slug"] = self.kwargs['slug']
        context["is_owner"] = Organization.objects.filter(slug=self.kwargs['slug'], owner=self.request.user).exists()
        return context


class AuctionCreateView(CreateView):
    template_name = "auctions/create_auction.html"
    model = Auction
    fields = ['name', 'description', 'start_time', 'end_time', 'optional_password']

    def get_success_url(self):
        return reverse_lazy('auction_plan', kwargs={'slug': self.kwargs['slug'], 'auction_id': self.object.id})

    def form_valid(self, form):
        self.object = form.save()
        org_instance = Organization.objects.get(slug=self.kwargs['slug'])
        org_instance.auctions.add(self.object)
        org_instance.save()
        return redirect(self.get_success_url())


class AuctionMixin(object):
    model = Auction

    def get_context_data(self, **kwargs):
        context = super(AuctionMixin, self).get_context_data(**kwargs)
        context["org_slug"] = self.kwargs['slug']
        return context

    def get_object(self, queryset=None):
        return Auction.objects.get(id=self.kwargs['auction_id'], auctions__slug=self.kwargs['slug'])


class AuctionPlanView(AuctionMixin, DetailView):
    template_name = "auctions/plan.html"

    def get_context_data(self, **kwargs):
        context = super(AuctionPlanView, self).get_context_data(**kwargs)
        context["items"] = self.object.bidables.filter(polymorphic_ctype__name="item")
        context["item_collections"] = self.object.bidables.filter(polymorphic_ctype__name="itemcollection")
        return context


class AuctionManageView(AuctionMixin, DetailView):
    template_name = "auctions/manage.html"


class AuctionClaimView(AuctionMixin, DetailView):
    template_name = "auctions/claim.html"

    def get_context_data(self, **kwargs):
        context = super(AuctionClaimView, self).get_context_data(**kwargs)
        context["unclaimed_items"] = self.object.bidables.filter(claimed=False)
        return context


class AuctionReportView(AuctionMixin, DetailView):
    template_name = "auctions/report.html"
