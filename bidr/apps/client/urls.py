"""
.. module:: bidr.apps.client.urls
   :synopsis: Bidr Silent Auction System Client Urls.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from .views import LoginView, AuctionListView, AddAuctionView, ItemListView, ItemDetailView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^$', login_required(AuctionListView.as_view(), login_url=reverse_lazy("client:login")), name="home"),
    url(r'^auctions/add/$', login_required(AddAuctionView.as_view(), login_url=reverse_lazy("client:login")), name="add_auction"),
    url(r'^client/auctions/(?P<auction_id>\d+)/list/$', login_required(ItemListView.as_view()), name='item_list'),
    url(r'^client/auctions/(?P<auction_id>\d+)/items/(?P<pk>\d+)/$', login_required(ItemDetailView.as_view()), name='item_detail')
]
