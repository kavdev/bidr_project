from django.contrib import admin

from .models import BidrUser


class BidrUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'email', 'phone_number', 'is_active', 'is_staff', 'is_superuser')

admin.site.register(BidrUser, BidrUserAdmin)
