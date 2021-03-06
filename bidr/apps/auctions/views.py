"""
.. module:: bidr.apps.auctions.views
   :synopsis: Bidr Silent Auction System Auction Views.

.. moduleauthor:: Jarred Stelfox <sstelfox@calpoly.edu>
.. moduleauthor:: Alexander Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView

from ..items.ajax import PopulateBidables
from ..items.models import ItemCollection, Item
from ..organizations.models import Organization
from .forms import ManagerForm, AuctionCreateForm
from .models import Auction, STAGES
from .utils import _end_auction


class AuctionView(TemplateView):
    template_name = "auctions/auctions.html"

    def get_context_data(self, **kwargs):
        context = super(AuctionView, self).get_context_data(**kwargs)
        context["upcoming_auctions"] = Auction.objects.filter(
            auctions__slug=self.kwargs['slug'],
            stage=STAGES.index("Plan")
        ).order_by("start_time")
        context["active_auctions"] = Auction.objects.filter(
            auctions__slug=self.kwargs['slug'],
            stage=STAGES.index("Observe")
        ).order_by("start_time")
        context["complete_auctions"] = Auction.objects.filter(
            auctions__slug=self.kwargs['slug'],
            stage__gte=STAGES.index("Claim")
        ).order_by("start_time")
        context["org_slug"] = self.kwargs['slug']
        context["org_name"] = Organization.objects.get(slug=self.kwargs['slug']).name
        context["is_owner"] = Organization.objects.filter(slug=self.kwargs['slug'], owner=self.request.user).exists()
        return context


class AuctionCreateView(CreateView):
    template_name = "auctions/create_auction.html"
    model = Auction
    form_class = AuctionCreateForm

    def get_success_url(self):
        return reverse_lazy('auction_plan', kwargs={'slug': self.kwargs['slug'], 'auction_id': self.object.id})

    def form_valid(self, form):
        self.object = form.save()
        org_instance = Organization.objects.get(slug=self.kwargs['slug'])
        org_instance.auctions.add(self.object)
        org_instance.save()
        messages.success(
            self.request,
            "The auction '{auction}' was successfully created.".format(auction=str(self.object))
        )
        return redirect(self.get_success_url())


class AuctionUpdateView(UpdateView):
    template_name = "auctions/update_auction.html"
    model = Auction
    form_class = AuctionCreateForm

    def form_valid(self, form):
        messages.success(
            self.request,
            "The auction '{auction}' was successfully updated.".format(auction=str(self.object))
        )
        return super(AuctionUpdateView, self).form_valid(form)

    def get_object(self, queryset=None):
        return Auction.objects.get(id=self.kwargs['auction_id'], auctions__slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse_lazy('update_auction', kwargs={'slug': self.kwargs['slug'], 'auction_id': self.object.id})


class AuctionManageView(FormView):
    template_name = "auctions/managers.html"
    form_class = ManagerForm

    def form_valid(self, form):
        manager_email = form.cleaned_data["manager_email"]
        manager_instance = get_user_model().objects.get(email=manager_email)
        auction_instance = Auction.objects.get(id=self.kwargs['auction_id'])
        auction_instance.managers.add(manager_instance)
        auction_instance.save()
        return super(AuctionManageView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AuctionManageView, self).get_context_data(**kwargs)
        context["org_slug"] = self.kwargs['slug']
        context["auction"] = Auction.objects.get(id=self.kwargs['auction_id'])
        return context

    def get_success_url(self):
        return reverse_lazy(
            'auction_managers',
            kwargs={'slug': self.kwargs['slug'], 'auction_id': self.kwargs['auction_id']}
        )


class AuctionMixin(object):
    model = Auction
    stage = None

    def dispatch(self, request, *args, **kwargs):
        auction = self.model.objects.get(id=kwargs["auction_id"])
        stage_map = ["auction_plan", "auction_observe", "auction_claim", "auction_report"]

        if auction.stage != self.stage:
            return redirect(stage_map[auction.stage], **kwargs)

        return super(AuctionMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AuctionMixin, self).get_context_data(**kwargs)
        context["org_slug"] = self.kwargs['slug']
        return context

    def get_object(self, queryset=None):
        return Auction.objects.get(id=self.kwargs['auction_id'], auctions__slug=self.kwargs['slug'])


class AuctionPlanView(AuctionMixin, DetailView):
    template_name = "auctions/plan.html"
    stage = STAGES.index("Plan")

    def get_context_data(self, **kwargs):
        context = super(AuctionPlanView, self).get_context_data(**kwargs)
        context["items"] = self.object.bidables.instance_of(Item).order_by("name")
        context["item_collections"] = self.object.bidables.instance_of(ItemCollection).order_by("name")
        return context


class AuctionObserveView(AuctionMixin, DetailView):
    template_name = "auctions/observe.html"
    stage = STAGES.index("Observe")

    def get_context_data(self, **kwargs):
        context = super(AuctionObserveView, self).get_context_data(**kwargs)
        context["datatables_class"] = PopulateBidables
        context["kwargs"] = self.kwargs
        return context


class AuctionClaimView(AuctionMixin, DetailView):
    template_name = "auctions/claim.html"
    stage = STAGES.index("Claim")

    def get_context_data(self, **kwargs):
        context = super(AuctionClaimView, self).get_context_data(**kwargs)
        context["unclaimed_items"] = self.object.bidables.filter(claimed=False).exclude(bids=None)
        return context


class AuctionReportView(AuctionMixin, DetailView):
    template_name = "auctions/report.html"
    stage = STAGES.index("Report")


def start_auction(request, slug, auction_id):
    auction_instance = Auction.objects.get(id=auction_id)
    auction_instance.start_time = timezone.now()
    auction_instance.stage = STAGES.index("Observe")
    auction_instance.save()
    return redirect('auction_observe', slug, auction_id)


def end_auction(request, slug, auction_id):
    auction_instance = Auction.objects.get(id=auction_id)
    new_stage = _end_auction(auction_instance)

    if new_stage == STAGES.index("Report"):
        return redirect('auction_report', slug, auction_id)
    elif new_stage == STAGES.index("Claim"):
        return redirect('auction_claim', slug, auction_id)
