"""
.. module:: bidr.apps.auctions.ajax
   :synopsis: Bidr Silent Auction System Auction AJAX Methods.

"""

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django_ajax.decorators import ajax

from ..items.models import ItemCollection, Item
from .models import Auction
from .views import end_auction


@ajax
@require_POST
def remove_manager(request, slug, auction_id):
    manager_id = request.POST["manager_id"]

    manager_instance = get_user_model().objects.get(id=manager_id)

    auction_instance = Auction.objects.get(id=auction_id)
    auction_instance.managers.remove(manager_instance)
    auction_instance.save()


@ajax
@require_POST
def can_start_auction(request, slug, auction_id):
    auction_instance = Auction.objects.get(id=auction_id)
    itemcollections = auction_instance.bidables.instance_of(ItemCollection)
    items = auction_instance.bidables.instance_of(Item)

    good_to_go = True
    message = ""

    # Are any of the collections empty?
    for item_collection in itemcollections:
        if not item_collection.items.all():
            good_to_go = False
            message = "The auction cannot start with an empty item collection."

    # Are there any items
    if not items.exists():
        good_to_go = False
        message = "The auction cannot start without any items."

    return {"success": good_to_go, "message": message}


@ajax
@require_POST
def check_time(request, slug, auction_id):
    current_time = now()
    auc_instance = Auction.objects.get(id=auction_id)

    if current_time > auc_instance.end_time:
        return end_auction(request, slug, auction_id)
