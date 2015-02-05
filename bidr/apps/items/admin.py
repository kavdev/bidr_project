from django.contrib import admin

from .models import Item, ItemCollection

admin.site.register(Item)
admin.site.register(ItemCollection)
