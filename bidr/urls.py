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
from rest_framework.authtoken import views

from .apps.bids.api import BidViewSet
from .apps.core.api import BidrUserViewSet
from .apps.core.views import IndexView, LoginView


admin.autodiscover()

bid_router = DefaultRouter()
bid_router.register(r'bids', BidViewSet)

bidruser_router = DefaultRouter()
bidruser_router.register(r'users', BidrUserViewSet)

logger = logging.getLogger(__name__)

# Core
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=static('img/favicon.ico')), name='favicon'),
    url(r'^flugzeug/', include(admin.site.urls)),  # admin site urls, masked
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api/', include(bidruser_router.urls)),
]

# Registration
urlpatterns += [
    url(r'^register/$', RedirectView.as_view(url='https://google.com'), name='register'),
]

# Bids
urlpatterns += [
    url(r'^api/', include(bid_router.urls)),
]
