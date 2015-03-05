"""
.. module:: bidr.apps.items.ajax
   :synopsis: Bidr Silent Auction System Item AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""
from django_ajax.decorators import ajax
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from ..auctions.models import Auction, STAGES
from ..bids.models import Bid
from .models import Item, ItemCollection
from bidr.apps.organizations.models import Organization


@ajax
@require_POST
def claim_item(request, slug, auction_id):
    item_id = request.POST["item_id"]
    bid_id = request.POST["bid_id"]

    item_instance = Item.objects.get(id=item_id)
    bid_instance = Bid.objects.get(id=bid_id)
    item_instance.claim(bid_instance)

    auction_instance = Auction.objects.get(id=auction_id)
    unclaimed_items = auction_instance.bidables.filter(claimed=False).exclude(bids=None)

    if not unclaimed_items:
        auction_instance.stage = STAGES.index("Report")
        auction_instance.save()
        return redirect('auction_report', slug, auction_id)


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

    auction_instance = Auction.objects.get(id=auction_id)
    item_collection_instance = ItemCollection.objects.get(id=itemcollection_id)

    # Move all collected items back into the auction's biddable items
    for item in item_collection_instance.items.all():
        auction_instance.bidables.add(item)
    auction_instance.save()
    item_collection_instance.items.clear()

    # Delete the item colleciton
    item_collection_instance.delete()


@ajax
@require_POST
def add_item_to_collection(request, slug, auction_id):
    item_id = request.POST["item_id"]
    new_itemcollection_id = request.POST["new_itemcollection_id"]
    old_itemcollection_id = request.POST.get("old_itemcollection_id")

    if old_itemcollection_id:
        # Move the collection item to a new collection
        old_item_collection_instance = ItemCollection.objects.get(id=old_itemcollection_id)
        old_item_collection_instance.items.remove(item_id)
        old_item_collection_instance.save()
    else:
        # Remove the single item from the auction's biddable items
        auction_instance = Auction.objects.get(id=auction_id)
        auction_instance.bidables.remove(item_id)
        auction_instance.save()

    # Add the item to the collection
    new_item_collection_instance = ItemCollection.objects.get(id=new_itemcollection_id)
    new_item_collection_instance.items.add(item_id)
    new_item_collection_instance.save()


@ajax
@require_POST
def remove_item_from_collection(request, slug, auction_id):
    item_id = request.POST["item_id"]
    itemcollection_id = request.POST["itemcollection_id"]

    # Remove the single item from the collection
    item_collection_instance = ItemCollection.objects.get(id=itemcollection_id)
    item_collection_instance.items.remove(item_id)
    item_collection_instance.save()

    # Add the single item back into the auction's biddable items
    auction_instance = Auction.objects.get(id=auction_id)
    auction_instance.bidables.add(item_id)
    auction_instance.save()
