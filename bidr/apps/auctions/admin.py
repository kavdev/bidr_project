from django.contrib import admin

from .models import Auction, AuctionUserInfo


admin.site.register(Auction)
admin.site.register(AuctionUserInfo)
