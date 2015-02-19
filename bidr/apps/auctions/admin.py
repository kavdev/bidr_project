from django.contrib import admin

from .models import Auction, AuctionUserInfo


class AuctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'stage')

admin.site.register(Auction, AuctionAdmin)
admin.site.register(AuctionUserInfo)
