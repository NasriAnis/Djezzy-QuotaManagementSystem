from django.contrib import admin

from .models import Client, Store, StoreOfferTransaction

admin.site.register(Client)
admin.site.register(Store)
admin.site.register(StoreOfferTransaction)