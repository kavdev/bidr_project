"""
.. module:: bidr.apps.items.ajax
   :synopsis: Bidr Silent Auction System Item AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.views.decorators.http import require_POST

from django_ajax.decorators import ajax

from ..bids.models import Bid
from ..items.models import Item, ItemCollection


@ajax
@require_POST
def claim_item(request, slug, auction_id):
    item_id = request.POST["item_id"]
    bid_id = request.POST["bid_id"]

    item_instance = Item.objects.get(id=item_id)
    bid_instance = Bid.objects.get(id=bid_id)
    item_instance.claim(bid_instance)


@ajax
@require_POST
def delete_item(request, slug, auction_id):
    item_id = request.POST["item_id"]

    item_instance = Item.objects.get(id=item_id)
    item_instance.delete()


@ajax
@require_POST
def delete_item_collection(request, slug, auction_id):
    itemcollection_id = request.POST["itemcollection_id"]

    item_collection_instance = ItemCollection.objects.get(id=itemcollection_id)
    item_collection_instance.delete()


@ajax
@require_POST
def remove_item_from_collection(request, slug, auction_id):
    item_id = request.POST["item_id"]
    itemcollection_id = request.POST["itemcollection_id"]

    item_collection_instance = ItemCollection.objects.get(id=itemcollection_id)
    item_collection_instance.items.remove(item_id)
    item_collection_instance.save()
