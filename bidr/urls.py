"""
.. module:: bidr.urls
   :synopsis: Bidr Silent Auction System URLs.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

import logging

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.templatetags.staticfiles import static as staticfiles
from django.views.defaults import permission_denied, page_not_found
from django.views.generic.base import RedirectView, TemplateView
from djoser import urls as api_auth_urls

from .apps.auctions.ajax import remove_manager, can_start_auction, check_time
from .apps.auctions.api import AddAuctionParticipantView, RetrieveAuctionAPIView, RetrieveAuctionItemView
from .apps.auctions.views import (AuctionView, AuctionCreateView, AuctionUpdateView, AuctionPlanView,
                                  AuctionManageView, AuctionObserveView, AuctionClaimView, AuctionReportView,
                                  start_auction, end_auction)
from .apps.bids.api import CreateBidAPIView
from .apps.client import urls as client_urls
from .apps.core.api import GetBidrUserParticipatedAuctionsView, UpdateUserIOSDeviceTokenView
from .apps.core.utils import user_is_type, UserType
from .apps.core.views import IndexView, LoginView, logout, handler500
from .apps.items.ajax import (claim_item, delete_item, add_item_to_collection, remove_item_from_collection,
                              delete_item_collection, PopulateBidables, remove_bid)
from .apps.items.api import RetrieveItemAPIView
from .apps.items.views import (ItemCreateView, ItemCollectionCreateView, ItemUpdateView, ItemCollectionUpdateView,
                               ItemModalView)
from .apps.organizations.views import OrganizationListView, OrganizationCreateView, OrganizationUpdateView


admin.autodiscover()

logger = logging.getLogger(__name__)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=staticfiles('img/favicon.ico')), name='favicon'),
    url(r'^robots\.txt$', RedirectView.as_view(url=staticfiles('robots.txt')), name='robots'),
    url(r'^zoidberg/', include(admin.site.urls)),  # admin site urls, masked
    url(r'^admin/', TemplateView.as_view(template_name="honeypot.html"), name="contact"),  # admin site urls, honeypot
    url(r'^login/$', LoginView.as_view(), name='admin_login'),
    url(r'^logout/$', logout, name='admin_logout'),

    url(r'^client/', include(client_urls, namespace="client")),
]

# API
urlpatterns += [
    url(r'^api/auth/', include(api_auth_urls)),
    url(r'^api/users/(?P<pk>\d+)/update_ios_device_token/$', UpdateUserIOSDeviceTokenView.as_view()),
    url(r'^api/users/(?P<pk>\d+)/auctions/$', GetBidrUserParticipatedAuctionsView.as_view()),
    url(r'^api/auctions/(?P<pk>\d+)/participants/add/$', AddAuctionParticipantView.as_view()),
    url(r'^api/auctions/(?P<pk>\d+)/$', RetrieveAuctionAPIView.as_view()),
    url(r'^api/auctions/(?P<pk>\d+)/items/$', RetrieveAuctionItemView.as_view()),
    url(r'^api/items/(?P<pk>\d+)/$', RetrieveItemAPIView.as_view()),
    url(r'^api/bids/create/$', CreateBidAPIView.as_view()),
]

# Organizations
urlpatterns += [
    url(r'^organizations/$', login_required(OrganizationListView.as_view()), name="organizations"),
    url(r'^organizations/create/$', login_required(OrganizationCreateView.as_view()), name="create_organization"),
    url(r'^organizations/update/(?P<slug>[\w-]+)/$', login_required(OrganizationUpdateView.as_view()),
        name="update_organization"),
]

# Auctions
urlpatterns += [
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/$', login_required(AuctionView.as_view()), name='auctions'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/create/$',
        login_required(user_is_type(UserType.MANAGER)(AuctionCreateView.as_view())), name='create_auction'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/update/(?P<auction_id>\d+)/$',
        login_required(user_is_type(UserType.MANAGER)(AuctionUpdateView.as_view())), name='update_auction'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/plan/$',
        login_required(user_is_type(UserType.MANAGER)(AuctionPlanView.as_view())), name='auction_plan'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/managers/$',
        login_required(user_is_type(UserType.MANAGER)(AuctionManageView.as_view())), name='auction_managers'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/managers/remove$',
        login_required(user_is_type(UserType.MANAGER)(remove_manager)), name='remove_manager'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/preflight-check/$',
        login_required(user_is_type(UserType.MANAGER)(can_start_auction)), name='preflight_check'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/start/$',
        login_required(user_is_type(UserType.MANAGER)(start_auction)), name='start_auction'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/observe/$',
        login_required(user_is_type(UserType.MANAGER)(AuctionObserveView.as_view())), name='auction_observe'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/observe/populate/$',
        login_required(user_is_type(UserType.MANAGER)(PopulateBidables.as_view())), name='populate_bidables'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/end/$',
        login_required(user_is_type(UserType.MANAGER)(end_auction)), name='end_auction'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/claim/$',
        login_required(user_is_type(UserType.MANAGER)(AuctionClaimView.as_view())), name='auction_claim'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/report/$',
        login_required(user_is_type(UserType.MANAGER)(AuctionReportView.as_view())), name='auction_report'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/check-time/$',
        login_required(user_is_type(UserType.MANAGER)(check_time)), name='check_time'),
]

# Items
urlpatterns += [
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/items/(?P<pk>\d+)/bid-modal/$',
        login_required(user_is_type(UserType.MANAGER)(ItemModalView.as_view())), name='bid_modal'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/items/create/$',
        login_required(user_is_type(UserType.MANAGER)(ItemCreateView.as_view())), name='create_item'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/items/update/(?P<pk>\d+)/$',
        login_required(user_is_type(UserType.MANAGER)(ItemUpdateView.as_view())), name='update_item'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/items/delete/$',
        login_required(user_is_type(UserType.MANAGER)(delete_item)), name='delete_item'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/itemcollections/create/$',
        login_required(user_is_type(UserType.MANAGER)(ItemCollectionCreateView.as_view())),
        name='create_item_collection'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/itemcollections/add-item/$',
        login_required(user_is_type(UserType.MANAGER)(add_item_to_collection)), name='add_item_to_collection'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/itemcollections/remove-item/$',
        login_required(user_is_type(UserType.MANAGER)(remove_item_from_collection)),
        name='remove_item_from_collection'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/itemcollections/update/(?P<pk>\d+)/$',
        login_required(user_is_type(UserType.MANAGER)(ItemCollectionUpdateView.as_view())),
        name='update_item_collection'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/itemcollections/delete/$',
        login_required(user_is_type(UserType.MANAGER)(delete_item_collection)), name='delete_item_collection'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/claim/claim-item/$',
        login_required(user_is_type(UserType.MANAGER)(claim_item)), name='claim_item'),
    url(r'^organizations/(?P<slug>[\w-]+)/auctions/(?P<auction_id>\d+)/claim/remove-highest-bid/$',
        login_required(user_is_type(UserType.MANAGER)(remove_bid)), name='remove_bid'),
]


# Hooks to intentionally raise errors
urlpatterns += [
    url(r'^500/$', handler500, name="500"),
    url(r'^403/$', permission_denied, name="403"),
    url(r'^404/$', page_not_found, name="404"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
