"""
.. module:: bidr.urls
   :synopsis: Bidr Silent Auction System URLs.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging

from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView

from rest_framework.routers import DefaultRouter

from .apps.bids.views import BidViewSet, get_max_bid
from .apps.core.views import BidderViewSet


admin.autodiscover()

bid_router = DefaultRouter()
bid_router.register(r'bids', BidViewSet)

bidder_router = DefaultRouter()
bidder_router.register(r'bidders', BidderViewSet)

logger = logging.getLogger(__name__)

# Core
urlpatterns = [
    url(r'^$', RedirectView.as_view(url="http://transitionvoice.com/wp-content/uploads/2011/08/ITS-all-good.png"), name='hello_world'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='%simages/icons/favicon.ico' % settings.STATIC_URL), name='favicon'),
    url(r'^flugzeug/', include(admin.site.urls)),  # admin site urls, masked
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(bidder_router.urls)),
]

# Bids
urlpatterns += [
    url(r'^api/', include(bid_router.urls)),
    url(r'^api/max_bid/$', get_max_bid, name="max_bid"),
]
