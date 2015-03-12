

@ajax
@require_POST
def delete_manager(request, slug, auction_id):
    item_id = request.POST["item_id"]

    item_instance = Item.objects.get(id=item_id)
    item_instance.delete()