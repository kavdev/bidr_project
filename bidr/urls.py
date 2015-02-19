"""
.. module:: bidr.urls
   :synopsis: Bidr Silent Auction System URLs.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.templatetags.staticfiles import static as staticfiles
from django.views.generic.base import RedirectView, TemplateView
from django.views.defaults import permission_denied, page_not_found

from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken import views
from djoser import urls as api_auth_urls

from .apps.bids.api import BidViewSet
from .apps.core.api import BidrUserViewSet

from .apps.auctions.views import AuctionView, AuctionCreateView, AuctionPlanView, AuctionManageView, AuctionClaimView, AuctionReportView
from .apps.core.views import IndexView, LoginView, logout, handler500
from .apps.organizations.views import OrganizationListView, OrganizationCreateView
from .apps.items.views import ItemCreateView

from .apps.items.ajax import claim_item, delete_item

from .apps.core.utils import user_is_type, UserType


admin.autodiscover()

bid_router = DefaultRouter()
bid_router.register(r'bids', BidViewSet)

bidruser_router = DefaultRouter()
bidruser_router.register(r'users', BidrUserViewSet)

logger = logging.getLogger(__name__)


# Core
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=staticfiles('img/favicon.ico')), name='favicon'),
    url(r'^robots\.txt$', RedirectView.as_view(url=staticfiles('robots.txt')), name='robots'),
    url(r'^flugzeug/', include(admin.site.urls)),  # admin site urls, masked
    url(r'^admin/$', TemplateView.as_view(template_name="honeypot.html"), name="contact"),  # admin site urls, honeypot
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
#     url(r'^api/token-auth/$', views.obtain_auth_token),
    url(r'^api/', include(bidruser_router.urls)),
    url(r'^login/$', LoginView.as_view(), name='admin_login'),
    url(r'^logout/$', logout, name='admin_logout'),
]

# Bids
urlpatterns += [
    url(r'^api/', include(bid_router.urls)),
]

# Registration
urlpatterns += [
    url(r'^api/', include(api_auth_urls))
]

# Organizations
urlpatterns += [
    url(r'^organizations/$', login_required(OrganizationListView.as_view()), name="organizations"),
    url(r'^organizations/create/$', login_required(user_is_type(UserType.OWNER)(OrganizationCreateView.as_view())), name="create_organization"),
]

# Auctions
urlpatterns += [
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/$', login_required(AuctionView.as_view()), name='auctions'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/create/$', login_required(user_is_type(UserType.MANAGER)(AuctionCreateView.as_view())), name='create_auction'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/plan/$', login_required(user_is_type(UserType.MANAGER)(AuctionPlanView.as_view())), name='auction_plan'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/manage/$', login_required(user_is_type(UserType.MANAGER)(AuctionManageView.as_view())), name='auction_manage'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/claim/$', login_required(user_is_type(UserType.MANAGER)(AuctionClaimView.as_view())), name='auction_claim'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/report/$', login_required(user_is_type(UserType.MANAGER)(AuctionReportView.as_view())), name='auction_report'),
]

# Items
urlpatterns += [
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/items/create/$', login_required(user_is_type(UserType.MANAGER)(ItemCreateView.as_view())), name='create_item'),
    url(r'organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/claim/claim-item/$', login_required(user_is_type(UserType.MANAGER)(claim_item)), name='claim_item'),
    url(r'organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/claim/delete-item/$', login_required(user_is_type(UserType.MANAGER)(delete_item)), name='delete_item'),
]

# Hooks to intentionally raise errors
urlpatterns += [
    url(r'^500/$', handler500, name="500"),
    url(r'^403/$', permission_denied, name="403"),
    url(r'^404/$', page_not_found, name="404"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
