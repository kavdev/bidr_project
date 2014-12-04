from django.contrib import admin

from .models import Bidder


class BidderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'is_active', 'is_staff', 'is_superuser')

admin.site.register(Bidder, BidderAdmin)
