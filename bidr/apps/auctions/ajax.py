from django_ajax.decorators import ajax
from django.views.decorators.http import require_POST

from ..auctions.models import Auction


@ajax
@require_POST
def is_one_collection_empty(request, slug, auction_id):
    auc_instance = Auction.objects.get(id=auction_id)
    itemcollections = auc_instance.bidables.filter(polymorphic_ctype__name="item collection").order_by("name")
    is_empty = False
    for item_collection in itemcollections:
        if not item_collection.items.all():
            is_empty = True

    if is_empty:
        return {"success": True}
    else:
        return {"success": False}
