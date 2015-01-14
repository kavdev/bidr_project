"""
.. module:: bidr.urls
   :synopsis: Bidr Silent Auction System URLs.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import RedirectView

from rest_framework.routers import DefaultRouter

from .apps.bids.api import BidViewSet
from .apps.core.api import BidrUserViewSet


admin.autodiscover()

bid_router = DefaultRouter()
bid_router.register(r'bids', BidViewSet)

bidruser_router = DefaultRouter()
bidruser_router.register(r'users', BidrUserViewSet)

logger = logging.getLogger(__name__)

# Core
urlpatterns = [
    url(r'^$', RedirectView.as_view(url="http://transitionvoice.com/wp-content/uploads/2011/08/ITS-all-good.png"), name='hello_world'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=static('images/icons/favicon.ico')), name='favicon'),
    url(r'^flugzeug/', include(admin.site.urls)),  # admin site urls, masked
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(bidruser_router.urls)),
]

# Bids
urlpatterns += [
    url(r'^api/', include(bid_router.urls)),
]
