"""
.. module:: bidr.apps.auctions.views
   :synopsis: Bidr Silent Auction System Auction Views.

.. moduleauthor:: Jarred Stelfox <sstelfox@calpoly.edu>
.. moduleauthor:: Alexander Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..auctions.models import STAGES
from ..organizations.models import Organization
from .models import Auction
from .forms import ManagerForm


class AuctionView(TemplateView):
    template_name = "auctions/auctions.html"

    def get_queryset(self):
        return Auction.objects.managed_by(self.request.user).filter(auctions__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(AuctionView, self).get_context_data(**kwargs)
        context["upcoming_auctions"] = Auction.objects.filter(stage=STAGES.index("Plan"))
        context["current_auctions"] = Auction.objects.filter(stage=STAGES.index("Observe"))
        context["complete_auctions"] = Auction.objects.filter(stage__gte=STAGES.index("Claim"))
        context["org_slug"] = self.kwargs['slug']
        context["org_name"] = Organization.objects.get(slug=self.kwargs['slug']).name
        context["is_owner"] = Organization.objects.filter(slug=self.kwargs['slug'], owner=self.request.user).exists()
        return context


class AuctionCreateView(CreateView):
    template_name = "auctions/create_auction.html"
    model = Auction
    fields = ['name', 'description', 'end_time', 'optional_password']

    def get_success_url(self):
        return reverse_lazy('auction_plan', kwargs={'slug': self.kwargs['slug'], 'auction_id': self.object.id})

    def form_valid(self, form):
        self.object = form.save()
        org_instance = Organization.objects.get(slug=self.kwargs['slug'])
        org_instance.auctions.add(self.object)
        org_instance.save()
        return redirect(self.get_success_url())


class AuctionUpdateView(UpdateView):
    template_name = "auctions/update_auction.html"
    model = Auction
    fields = ['name', 'description', 'end_time', 'optional_password']

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
        return reverse_lazy('auction_managers', kwargs={'slug': self.kwargs['slug'], 'auction_id': self.kwargs['auction_id']})


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
        context["items"] = self.object.bidables.filter(polymorphic_ctype__name="item").order_by("name")
        context["item_collections"] = self.object.bidables.filter(polymorphic_ctype__name="item collection").order_by("name")
        return context


class AuctionObserveView(AuctionMixin, DetailView):
    template_name = "auctions/observe.html"
    stage = STAGES.index("Observe")


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
    auc_instance = Auction.objects.get(id=auction_id)
    auc_instance.start_time = timezone.now()
    auc_instance.stage = STAGES.index("Observe")
    auc_instance.save()
    return redirect('auction_observe', slug, auction_id)


def end_auction(request, slug, auction_id):
    auc_instance = Auction.objects.get(id=auction_id)
    auc_instance.stage = STAGES.index("Claim")
    auc_instance.save()
    return redirect('auction_claim', slug, auction_id)
