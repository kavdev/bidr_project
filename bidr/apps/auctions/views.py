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
        return reverse_lazy('plan_auction', kwargs={'slug': self.kwargs['slug'], 'pk': self.object.id})


class AuctionPlanView(DetailView):
    template_name = "auctions/plan.html"
    model = Auction


class AuctionManageView(DetailView):
    template_name = "auctions/manage.html"
    model = Auction


class AuctionClaimView(DetailView):
    template_name = "auctions/claim.html"
    model = Auction


class AuctionReportView(DetailView):
    template_name = "auctions/plan.html"
    model = Auction
