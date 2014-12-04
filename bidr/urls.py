"""
.. module:: bidr.urls
   :synopsis: Bidr Silent Auction System URLs.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging

from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

logger = logging.getLogger(__name__)

# Core
urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url="http://transitionvoice.com/wp-content/uploads/2011/08/ITS-all-good.png"), name='hello_world'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='%simages/icons/favicon.ico' % settings.STATIC_URL), name='favicon'),
)

