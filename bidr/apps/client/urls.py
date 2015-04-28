"""
.. module:: bidr.apps.client.urls
   :synopsis: Bidr Silent Auction System Client Urls.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from .views import LoginView, AuctionListView

urlpatterns = [
    url(r'^$', login_required(AuctionListView.as_view(), login_url=reverse_lazy("client:login")), name="home"),
    url(r'^login/$', LoginView.as_view(), name="login"),
]
