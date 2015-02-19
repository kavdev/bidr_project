"""
.. module:: bidr.apps.auctions.ajax
   :synopsis: Bidr Silent Auction System AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.views.decorators.http import require_POST

from django_ajax.decorators import ajax

from bidr.apps.items.models import Item


@ajax
@require_POST
def claim_item(request):
    item_id = request.POST["item_id"]

    item_instance = Item.objects.get(id=item_id)
    item_instance.claim()
