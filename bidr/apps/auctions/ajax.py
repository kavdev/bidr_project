
from django.contrib.auth import get_user_model
from django_ajax.decorators import ajax
from django.views.decorators.http import require_POST

from ..auctions.models import Auction


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
