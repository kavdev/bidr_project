"""
.. module:: bidr.urls
   :synopsis: Bidr Silent Auction System URLs.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic.base import RedirectView, TemplateView
from django.views.defaults import permission_denied, page_not_found

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .apps.bids.api import BidViewSet
from .apps.core.api import BidrUserViewSet, RegisterBidrUser
from .apps.core.views import IndexView, LoginView, logout, handler500
from .apps.organizations.views import OrganizationListView
from .apps.auctions.views import AuctionView

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
    url(r'^robots\.txt$', RedirectView.as_view(url=static('robots.txt')), name='robots'),
    url(r'^flugzeug/', include(admin.site.urls)),  # admin site urls, masked
    url(r'^admin$', TemplateView.as_view(template_name="honeypot.html"), name="contact"),  # admin site urls, honeypot
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token-auth/', views.obtain_auth_token),
    url(r'^api/', include(bidruser_router.urls)),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
]

# Registration
urlpatterns += [
    url(r'api/users/register/', RegisterBidrUser.as_view())
]

# Bids
urlpatterns += [
    url(r'^api/', include(bid_router.urls)),
]

# Organizations
urlpatterns += [
    url(r'^organizations/', login_required(OrganizationListView.as_view()), name="organizations"),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/', AuctionView.as_view(), name='auctions'),
]

# Hooks to intentionally raise errors
urlpatterns += [
    url(r'^500/$', handler500, name="500"),
    url(r'^403/$', permission_denied, name="403"),
    url(r'^404/$', page_not_found, name="404"),
]
