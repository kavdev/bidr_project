"""
.. module:: bidr.apps.items.ajax
   :synopsis: Bidr Silent Auction System Item AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

from collections import OrderedDict

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from django_ajax.decorators import ajax

from ..auctions.models import Auction, STAGES
from ..bids.models import Bid
from ..core.templatetags.currency import currency
from ..datatables.ajax import BidrDatatablesPopulateView
from .models import AbstractItem, Item, ItemCollection
from django.core.context_processors import request


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
def remove_bid(request, slug, auction_id):
    bid_id = request.POST["bid_id"]
    bid_instance = Bid.objects.get(id=bid_id)
    bid_instance.delete()


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


class PopulateBidables(BidrDatatablesPopulateView):
    """Renders the observe table."""

    # Hacking the crap out of the columns. Claimed is really image_urls, claimed_bid is really highest_bid
    column_definitions = OrderedDict()
    column_definitions["id"] = {"width": "0px", "searchable": False, "orderable": False, "visible": False, "title": "ID"}
    column_definitions["claimed"] = {"width": "225px", "type": "html", "title": "Item Picture", "searchable": False, "orderable": False, "sortable": False}
    column_definitions["name"] = {"width": "100px", "type": "string", "title": "Item Name"}
    column_definitions["description"] = {"width": "225px", "type": "string", "title": "Description"}
    column_definitions["claimed_bid"] = {"width": "100px", "type": "string", "title": "Current Highest Bid", "searchable": False, "orderable": False}

    def get_initial_queryset(self):
        return Auction.objects.get(id=self.kwargs["auction_id"], auctions__slug=self.kwargs["slug"]).bidables.all()

    def get_data_source(self):
        return reverse('populate_bidables', kwargs=self.kwargs)

    def get_row_id(self, row):
        return "row_" + str(row.id)

    def get_row_class(self, row):
        return "hyperlinked_row"

    def get_row_data_attributes(self, row):
        return {"data-toggle": "modal", "data-target": "#item_modal_" + str(row.id)}

    def render_column(self, row, column):
        if column == 'claimed':
            html = ""

            for image_url in row.image_urls:
                html += """<img src="{image_url}" alt="Item Picture" height="100px">""".format(image_url=image_url)

            return html
        elif column == 'claimed_bid':
            if row.highest_bid:
                return currency(row.highest_bid.amount)
            else:
                return ""
        else:
            return super(PopulateBidables, self).render_column(row, column)
