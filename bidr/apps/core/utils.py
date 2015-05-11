"""
.. module:: bidr.apps.core.utils
   :synopsis: Bidr Silent Auction System Core Utilities.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.cache import cache
from django.utils.decorators import available_attrs
from django.utils.encoding import force_str
from django.shortcuts import resolve_url

from ..organizations.models import Organization
from ..auctions.models import Auction


class UserType(object):
    SUPERUSER = 0
    OWNER = 1
    MANAGER = 2


def user_is_type(user_type, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is of the passed user type,
    redirecting to the log-in page if necessary.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if user_type_test(user_type=user_type, user=request.user, org_slug=kwargs["slug"], auction_id=kwargs.get("auction_id")):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            # urlparse chokes on lazy objects in Python 3, force to str
            resolved_login_url = force_str(
                resolve_url(login_url or settings.LOGIN_URL))
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def user_type_test(user_type, user, org_slug, auction_id=None):
    """
    Checks if the user is of a specific type for permission handling.

    If an auction_id is passed in, the user is also checked against an auction's manager list.

    """

    # Catch anonymous users
    if user.is_anonymous():
        return False

    # Cache must be per organization (and, optionally, per auction)
    cache_org_slug = org_slug
    cache_auction_id = auction_id

    cache_key = "usertype:{org}:{auction}:{username}:{usertype}::".format(org=cache_org_slug,
                                                                          auction=cache_auction_id,
                                                                          username=user.get_username(),
                                                                          usertype=str(user_type))

    # Check if the lookup has already occurred
    is_user_type = cache.get(cache_key)

    if is_user_type is not None:
        return is_user_type
    else:
        org_instance = Organization.objects.get(slug=org_slug)

        if user_type == UserType.SUPERUSER:
            value = user.is_superuser
        elif user_type == UserType.OWNER:
            value = user.is_superuser or user == org_instance.owner
        elif user_type == UserType.MANAGER:
            value = user.is_superuser or user == org_instance.owner

            if auction_id:
                value = value or Auction.objects.filter(id=auction_id, managers__in=[user]).exists()
            else:
                value = value or user in org_instance.managers
        else:
            value = False

        cache.set(cache_key, value)
        return value
