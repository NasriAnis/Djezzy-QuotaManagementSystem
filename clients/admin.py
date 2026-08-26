from django.contrib import admin

from .models import Client, Store

admin.site.register(Client)
admin.site.register(Store)