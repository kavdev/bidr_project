"""
.. module:: bidr.apps.client.views
   :synopsis: Bidr Silent Auction System Client Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from ..auctions.models import Auction


class LoginView(FormView):
    template_name = "client/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("client:home")


class AuctionListView(ListView):
    template_name = "client/auction_list.html"
    model = Auction

    def get_queryset(self):
        return self.request.user.get_auctions_participated_in()
