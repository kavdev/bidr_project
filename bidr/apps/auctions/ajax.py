"""
.. module:: bidr.apps.auctions.ajax
   :synopsis: Bidr Silent Auction System AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.views.decorators.http import require_POST

from django_ajax.decorators import ajax

from ..bids.models import Bid
from ..items.models import Item


@ajax
@require_POST
def claim_item(request, slug, auction_id):
    item_id = request.POST["item_id"]
    bid_id = request.POST["bid_id"]

    item_instance = Item.objects.get(id=item_id)
    bid_instance = Bid.objects.get(id=bid_id)
    item_instance.claim(bid_instance)
