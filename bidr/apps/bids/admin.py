from django.contrib import admin

from .models import Bid


class BidAdmin(admin.ModelAdmin):
    list_display = ('amount', 'user', 'timestamp')


admin.site.register(Bid, BidAdmin)
